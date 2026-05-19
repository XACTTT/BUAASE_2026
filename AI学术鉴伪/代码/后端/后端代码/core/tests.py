import io
import shutil
import sys
import tempfile
from unittest.mock import patch

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from core.models import (
    DetectionTask,
    FileManagement,
    ImageUpload,
    Organization,
    ResourceContainer,
    ReviewTextResource,
    StructuredDetectionResult,
    TextDetectionResult,
)
from core.services.bert_text_ai_bridge import BertTextAIDetectionBridge
from core.services.fast_detect_gpt_ai_bridge import FastDetectGPTAIDetectionBridge
from core.tasks_new import (
    finalize_text_task,
    process_single_text_result,
    process_single_fast_detect_gpt_result,
    process_text_detection_task,
    run_structured_detection_task,
)


class ResourceManagementApiTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.mkdtemp(prefix='resource-media-')
        self.override = override_settings(MEDIA_ROOT=self.media_dir)
        self.override.enable()

        self.client = APIClient()
        self.organization = Organization.objects.create(name='Org A', email='org-a@example.com')
        self.user = get_user_model().objects.create_user(
            username='publisher',
            email='publisher@example.com',
            password='pass1234',
            organization=self.organization,
            role='publisher',
        )
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media_dir, ignore_errors=True)

    def _png_upload(self, name='sample.png'):
        buffer = io.BytesIO()
        image = Image.new('RGB', (8, 8), color=(255, 0, 0))
        image.save(buffer, format='PNG')
        return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')

    def _txt_upload(self, name='sample.txt', content='line 1\n\nline 2'):
        return SimpleUploadedFile(name, content.encode('utf-8'), content_type='text/plain')

    def test_container_crud(self):
        create_resp = self.client.post(
            '/api/resource-containers/',
            {'container_type': 'paper', 'title': 'Manuscript A', 'description': 'round 1'},
            format='json',
        )
        self.assertEqual(create_resp.status_code, 201)
        container_id = create_resp.data['id']

        list_resp = self.client.get('/api/resource-containers/')
        self.assertEqual(list_resp.status_code, 200)
        self.assertGreaterEqual(len(list_resp.data), 1)

        update_resp = self.client.put(
            f'/api/resource-containers/{container_id}/',
            {'title': 'Manuscript A v2', 'status': 'uploaded', 'progress_status': 'ready'},
            format='json',
        )
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.data['title'], 'Manuscript A v2')

        detail_resp = self.client.get(f'/api/resource-containers/{container_id}/')
        self.assertEqual(detail_resp.status_code, 200)

        delete_resp = self.client.delete(f'/api/resource-containers/{container_id}/')
        self.assertEqual(delete_resp.status_code, 204)

    def test_upload_endpoint_compatibility_with_and_without_container_id(self):
        no_container_resp = self.client.post('/api/upload/', {'file': self._png_upload('no_container.png')})
        self.assertEqual(no_container_resp.status_code, 200)
        self.assertIsNone(FileManagement.objects.get(id=no_container_resp.data['file_id']).container_id)

        container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='paper',
            title='Paper container',
        )

        with_container_resp = self.client.post(
            '/api/upload/',
            {
                'file': self._png_upload('with_container.png'),
                'container_id': container.id,
                'resource_role': 'paper_main',
                'batch_id': 'batch-1',
            },
        )
        self.assertEqual(with_container_resp.status_code, 200)

        file_record = FileManagement.objects.get(id=with_container_resp.data['file_id'])
        self.assertEqual(file_record.container_id, container.id)
        self.assertEqual(file_record.resource_role, 'paper_main')
        self.assertEqual(file_record.parse_status, 'parsed')
        self.assertTrue(ImageUpload.objects.filter(container=container).exists())

    def test_review_text_api_success_and_validation(self):
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        paper_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='paper',
            title='Paper Container',
        )

        success_resp = self.client.post(
            f'/api/resource-containers/{review_container.id}/review-text/',
            {'source_type': 'paste', 'language': 'zh', 'raw_text': 'review content'},
            format='json',
        )
        self.assertEqual(success_resp.status_code, 201)

        empty_resp = self.client.post(
            f'/api/resource-containers/{review_container.id}/review-text/',
            {'source_type': 'paste', 'language': 'zh', 'raw_text': '  '},
            format='json',
        )
        self.assertEqual(empty_resp.status_code, 400)
        self.assertEqual(empty_resp.data['error_code'], 'EMPTY_REVIEW_TEXT')

        wrong_type_resp = self.client.post(
            f'/api/resource-containers/{paper_container.id}/review-text/',
            {'source_type': 'paste', 'language': 'zh', 'raw_text': 'abc'},
            format='json',
        )
        self.assertEqual(wrong_type_resp.status_code, 400)
        self.assertEqual(wrong_type_resp.data['error_code'], 'INVALID_CONTAINER_TYPE')

    @patch('core.views.views_dectection.process_text_detection_task.apply_async')
    def test_submit_text_detection_enqueues_task(self, mocked_apply_async):
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        review_text = ReviewTextResource.objects.create(
            container=review_container,
            source_type='paste',
            language='zh',
            raw_text='这是一段需要检测的评审文本',
            normalized_text='这是一段需要检测的评审文本',
            token_count=1,
            parse_status='parsed',
        )

        response = self.client.post(
            '/api/detection/submit_text/',
            {
                'task_name': 'review-text-check',
                'task_type': 'review_text',
                'resource_ids': [review_text.id],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        task = DetectionTask.objects.get(id=response.data['task_id'])
        self.assertEqual(task.task_type, 'review_text')
        self.assertEqual(task.detect_type, 'review')
        self.assertTrue(
            TextDetectionResult.objects.filter(detection_task=task, text_resource=review_text).exists()
        )
        mocked_apply_async.assert_called_once()

    @patch('core.views.views_dectection.process_text_detection_task.apply_async')
    def test_submit_text_detection_accepts_file_ids_and_creates_review_text_resource(self, mocked_apply_async):
        upload_resp = self.client.post(
            '/api/upload/',
            {
                'file': self._txt_upload('review.txt', '第一段内容\n\n第二段内容'),
                'resource_role': 'review_main',
            },
        )
        self.assertEqual(upload_resp.status_code, 200)
        file_id = upload_resp.data['file_id']

        response = self.client.post(
            '/api/detection/submit_text/',
            {
                'task_name': 'review-from-file',
                'task_type': 'review_text',
                'file_ids': [file_id],
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        task = DetectionTask.objects.get(id=response.data['task_id'])
        self.assertEqual(task.task_type, 'review_text')
        self.assertEqual(task.detect_type, 'review')
        self.assertIsNotNone(task.container_id)

        created_review_text = ReviewTextResource.objects.filter(container_id=task.container_id).first()
        self.assertIsNotNone(created_review_text)
        self.assertEqual(created_review_text.source_type, 'file_parsed')
        self.assertIn('第一段内容', created_review_text.raw_text)
        self.assertTrue(
            TextDetectionResult.objects.filter(
                detection_task=task,
                text_resource=created_review_text,
            ).exists()
        )
        mocked_apply_async.assert_called_once()

    @patch('core.tasks_new.BertTextAIDetectionBridge.submit_text')
    def test_process_single_text_result_stores_bert_result(self, mocked_submit_text):
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        review_text = ReviewTextResource.objects.create(
            container=review_container,
            source_type='paste',
            language='zh',
            raw_text='这是一段需要检测的评审文本',
            normalized_text='这是一段需要检测的评审文本',
            token_count=1,
            parse_status='parsed',
        )
        task = DetectionTask.objects.create(
            organization=self.organization,
            user=self.user,
            task_name='review-text-check',
            task_type='review_text',
            status='in_progress',
        )
        result = TextDetectionResult.objects.create(
            detection_task=task,
            text_resource=review_text,
            status='in_progress',
        )
        mocked_submit_text.return_value = {
            'is_aigc': True,
            'label_name': 'aigc',
            'confidence_score': 0.93,
            'probabilities': {
                'human': 0.07,
                'aigc': 0.93,
            },
            'input_summary': {
                'pair_mode': False,
                'text_length': 12,
                'max_length': 256,
            },
        }

        ok = process_single_text_result(result.id, review_text.normalized_text, True)
        self.assertTrue(ok)

        result.refresh_from_db()
        self.assertEqual(result.status, 'completed')
        self.assertTrue(result.is_fake)
        self.assertEqual(result.confidence_score, 0.93)
        self.assertEqual(result.template_tendency_score, 0.93)
        self.assertIn('AIGC 概率', result.template_analysis_reason)

    @patch('core.tasks_new.chord')
    @patch('core.tasks_new.group')
    def test_process_text_detection_task_routes_subtasks_to_ai_queue(self, mocked_group, mocked_chord):
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        review_text = ReviewTextResource.objects.create(
            container=review_container,
            source_type='paste',
            language='zh',
            raw_text='这是一段需要检测的评审文本',
            normalized_text='这是一段需要检测的评审文本',
            token_count=1,
            parse_status='parsed',
        )
        task = DetectionTask.objects.create(
            organization=self.organization,
            user=self.user,
            task_name='review-text-check',
            task_type='review_text',
            status='pending',
        )
        result = TextDetectionResult.objects.create(
            detection_task=task,
            text_resource=review_text,
            status='pending',
        )

        chord_result = mocked_chord.return_value

        process_text_detection_task.run([result.id], task.id, True)

        mocked_group.assert_called_once()
        header_tasks = mocked_group.call_args.args
        self.assertEqual(len(header_tasks), 1)
        self.assertEqual(header_tasks[0].options.get('queue'), 'ai')

        mocked_chord.assert_called_once()
        body_signature = mocked_chord.call_args.args[1]
        self.assertEqual(body_signature.options.get('queue'), 'ai')
        chord_result.delay.assert_called_once()

        result.refresh_from_db()
        task.refresh_from_db()
        self.assertEqual(result.status, 'in_progress')
        self.assertEqual(task.status, 'in_progress')

    @patch.object(BertTextAIDetectionBridge, '_submit_local')
    @patch.object(BertTextAIDetectionBridge, '_submit_remote')
    @patch.object(BertTextAIDetectionBridge, '_can_use_local_mode', return_value=False)
    @patch.object(BertTextAIDetectionBridge, '_config')
    def test_bert_bridge_auto_mode_falls_back_to_ssh(
        self,
        mocked_config,
        mocked_can_use_local_mode,
        mocked_submit_remote,
        mocked_submit_local,
    ):
        mocked_config.return_value = {
            'mode': 'auto',
            'service_root': '/tmp/nonexistent-service-root',
            'request_filename': 'request.json',
            'ready_marker': 'ai service ready',
            'result_marker': 'ai service result',
            'connect_timeout': 10.0,
            'ready_timeout': 60.0,
            'result_timeout': 300.0,
            'submit_retry': 1,
            'host': '127.0.0.1',
            'port': 22,
            'username': 'tester',
            'password': 'secret',
            'remote_request_dir': '/tmp/requests',
            'remote_command': 'python trigger_unified.py',
            'local_python': sys.executable,
            'bert_project_root': '/tmp/checkpoints',
            'bert_text_model_dir': '',
        }
        mocked_submit_remote.return_value = {
            'is_aigc': False,
            'confidence_score': 0.12,
            'probabilities': {'human': 0.88, 'aigc': 0.12},
        }

        result = BertTextAIDetectionBridge.submit_text('test review text', language='zh')

        self.assertFalse(result['is_aigc'])
        mocked_can_use_local_mode.assert_called_once()
        mocked_submit_remote.assert_called_once()
        mocked_submit_local.assert_not_called()

    def test_bert_bridge_single_text_payload_uses_answer_field(self):
        payload = BertTextAIDetectionBridge._build_request_payload('test review text', language='zh', max_length=128)

        self.assertEqual(payload['pipeline'], 'bert')
        self.assertEqual(payload['payload']['lang'], 'chinese')
        self.assertEqual(payload['payload']['answer'], 'test review text')
        self.assertNotIn('text', payload['payload'])
        self.assertEqual(payload['payload']['max_length'], 128)

    def test_fast_detect_gpt_bridge_builds_fast_detect_payload(self):
        payload = FastDetectGPTAIDetectionBridge._build_request_payload('test review text', max_length=256)

        self.assertEqual(payload['pipeline'], 'fast_detect_gpt')
        self.assertEqual(payload['payload']['text'], 'test review text')
        self.assertEqual(payload['payload']['max_length'], 256)

    @patch('core.tasks_new.FastDetectGPTAIDetectionBridge.submit_text')
    def test_process_single_fast_detect_gpt_result_stores_result(self, mocked_submit_text):
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        review_text = ReviewTextResource.objects.create(
            container=review_container,
            source_type='paste',
            language='zh',
            raw_text='这是一段需要检测的评审文本',
            normalized_text='这是一段需要检测的评审文本',
            token_count=1,
            parse_status='parsed',
        )
        task = DetectionTask.objects.create(
            organization=self.organization,
            user=self.user,
            task_name='review-text-check',
            task_type='review_text',
            status='in_progress',
        )
        result = TextDetectionResult.objects.create(
            detection_task=task,
            text_resource=review_text,
            status='in_progress',
        )
        mocked_submit_text.return_value = {
            'is_aigc': False,
            'label_name': 'human',
            'confidence_score': 0.91,
            'probabilities': {
                'human': 0.91,
                'aigc': 0.09,
            },
            'input_summary': {
                'text_length': 12,
            },
        }

        ok = process_single_fast_detect_gpt_result(result.id, review_text.normalized_text, True)
        self.assertTrue(ok)

        result.refresh_from_db()
        self.assertEqual(result.status, 'completed')
        self.assertFalse(result.is_fake)
        self.assertEqual(result.confidence_score, 0.91)
        self.assertIn('FastDetectGPT', result.template_analysis_reason)

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        CELERY_TASK_EAGER_PROPAGATES=True,
        CHANNEL_LAYERS={'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}},
    )
    @patch('core.tasks_new.FastDetectGPTAIDetectionBridge.submit_text')
    def test_submit_text_detection_fast_detect_gpt_e2e_with_celery(self, mocked_submit_text):
        mocked_submit_text.return_value = {
            'project_root': '/mnt/data/ccy/Bert/fast-detect-gpt',
            'python': '/mnt/data14/ccy/pip_packs/miniconda3/envs/fast-detect-gpt/bin/python',
            'sampling_model_name': 'falcon-7b',
            'scoring_model_name': 'falcon-7b',
            'is_aigc': False,
            'label': 0,
            'label_name': 'human',
            'confidence_score': 0.9071478391683363,
            'probabilities': {
                'human': 0.9071478391683363,
                'aigc': 0.09285216083166364,
            },
            'fast_detect_gpt': {
                'criterion': -2.279296875,
                'token_count': 23,
                'max_length': 256,
                'load_in_8bit': False,
                'load_in_4bit': False,
            },
            'input_summary': {
                'question_length': 0,
                'text_length': 138,
            },
        }
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        review_text = ReviewTextResource.objects.create(
            container=review_container,
            source_type='paste',
            language='en',
            raw_text='This paragraph uses polished, highly uniform academic phrasing.',
            normalized_text='This paragraph uses polished, highly uniform academic phrasing.',
            token_count=8,
            parse_status='parsed',
        )

        response = self.client.post(
            '/api/detection/submit_text/',
            {
                'task_name': 'fast-detect-gpt-review-check',
                'task_type': 'review_text',
                'resource_ids': [review_text.id],
                'detection_mode': 'fast_detect_gpt',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        task = DetectionTask.objects.get(id=response.data['task_id'])
        text_result = TextDetectionResult.objects.get(detection_task=task, text_resource=review_text)

        mocked_submit_text.assert_called_once_with(text=review_text.normalized_text)
        task.refresh_from_db()
        text_result.refresh_from_db()
        self.assertEqual(task.status, 'completed')
        self.assertEqual(text_result.status, 'completed')
        self.assertFalse(text_result.is_fake)
        self.assertEqual(text_result.confidence_score, 0.9071478391683363)
        self.assertEqual(text_result.template_tendency_score, 0.9071478391683363)
        self.assertIn('FastDetectGPT', text_result.template_analysis_reason)

    def test_material_validation_pass_and_fail(self):
        container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='multi_material',
            title='MM Container',
        )

        fail_resp = self.client.post(f'/api/resource-containers/{container.id}/validate-materials/')
        self.assertEqual(fail_resp.status_code, 200)
        self.assertFalse(fail_resp.data['valid'])

        self.client.post(
            '/api/upload/',
            {
                'file': self._png_upload('material.png'),
                'container_id': container.id,
                'resource_role': 'paper_main',
            },
        )

        pass_resp = self.client.post(f'/api/resource-containers/{container.id}/validate-materials/')
        self.assertEqual(pass_resp.status_code, 200)
        self.assertTrue(pass_resp.data['valid'])

    def test_extract_contents_supports_txt(self):
        upload_resp = self.client.post('/api/upload/', {'file': self._txt_upload('paper.txt', 'first block\n\nsecond block')})
        self.assertEqual(upload_resp.status_code, 200)

        contents_resp = self.client.get(f"/api/upload/{upload_resp.data['file_id']}/extract_contents/")
        self.assertEqual(contents_resp.status_code, 200)
        self.assertEqual(contents_resp.data['total'], 2)
        self.assertEqual(contents_resp.data['contents'][0]['text'], 'first block')

    @patch('core.services.bert_text_ai_bridge.BertTextAIDetectionBridge.submit_batch')
    @patch('core.views.views_dectection.run_structured_detection_task.apply_async')
    def test_submit_paper_detection_and_fetch_structured_result(self, mocked_apply_async, mocked_submit_batch):
        mocked_submit_batch.return_value = {
            'batch_results': [
                {
                    'item_id': 'paper_0_0',
                    'is_aigc': True,
                    'label_name': 'aigc',
                    'confidence_score': 0.91,
                    'probabilities': {'human': 0.09, 'aigc': 0.91},
                },
            ],
            'aggregate': {
                'aigc_ratio': 1.0,
                'mean_aigc_probability': 0.91,
                'mean_confidence': 0.91,
                'max_confidence': 0.91,
                'min_confidence': 0.91,
            },
            'model_dir': '/tmp/test',
            'lang': 'chinese',
        }
        upload_resp = self.client.post(
            '/api/upload/',
            {
                'file': self._txt_upload('paper.txt', 'abstract text\n\nmethod text'),
                'resource_role': 'paper_main',
            },
        )
        self.assertEqual(upload_resp.status_code, 200)

        submit_resp = self.client.post(
            '/api/detection/submit/',
            {
                'mode': 2,
                'detect_type': 'paper',
                'task_name': 'paper-check',
                'file_ids': [upload_resp.data['file_id']],
            },
            format='json',
        )
        self.assertEqual(submit_resp.status_code, 200)
        task_id = submit_resp.data['task_id']

        task = DetectionTask.objects.get(id=task_id)
        run_structured_detection_task(task.id)
        task.refresh_from_db()

        self.assertEqual(task.detect_type, 'paper')
        self.assertEqual(task.status, 'completed')
        self.assertTrue(StructuredDetectionResult.objects.filter(detection_task=task).exists())

        result_resp = self.client.get(f'/api/tasks/{task_id}/structured-result/')
        self.assertEqual(result_resp.status_code, 200)
        self.assertEqual(result_resp.data['detect_type'], 'paper')
        self.assertIn('dimensions', result_resp.data['result'])

    def test_structured_result_for_review_text_task_uses_container_type_as_text_type(self):
        review_container = ResourceContainer.objects.create(
            organization=self.organization,
            owner=self.user,
            container_type='review',
            title='Review Container',
        )
        review_text = ReviewTextResource.objects.create(
            container=review_container,
            source_type='paste',
            language='zh',
            raw_text='这是一段需要检测的评审文本',
            normalized_text='这是一段需要检测的评审文本',
            token_count=1,
            parse_status='parsed',
        )
        task = DetectionTask.objects.create(
            organization=self.organization,
            user=self.user,
            task_name='review-text-check',
            task_type='review_text',
            status='completed',
            container=review_container,
        )
        TextDetectionResult.objects.create(
            detection_task=task,
            text_resource=review_text,
            status='completed',
            is_fake=False,
            confidence_score=0.91,
            template_tendency_score=0.91,
        )

        result_resp = self.client.get(f'/api/tasks/{task.id}/structured-result/')
        self.assertEqual(result_resp.status_code, 200)
        self.assertEqual(result_resp.data['detect_type'], 'review')
        self.assertEqual(result_resp.data['task_type'], 'review_text')
        self.assertEqual(result_resp.data['results'][0]['text_type'], 'review')
