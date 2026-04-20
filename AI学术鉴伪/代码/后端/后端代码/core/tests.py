import io
import shutil
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from core.models import FileManagement, ImageUpload, Organization, ResourceContainer


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