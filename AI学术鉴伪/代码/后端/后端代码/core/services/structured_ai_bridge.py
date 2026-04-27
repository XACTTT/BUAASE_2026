import base64
import json
import logging
import os
import tempfile
import time

import paramiko
from scp import SCPClient


logger = logging.getLogger(__name__)


class StructuredAIError(RuntimeError):
    pass


class StructuredAITransientError(StructuredAIError):
    pass


class StructuredAIPermanentError(StructuredAIError):
    pass


class StructuredAIDetectionBridge:
    REMOTE_ROOT = os.getenv('STRUCTURED_AI_REMOTE_ROOT', '/root/autodl-tmp/BUAA_SE_DetectFake')
    REMOTE_REQUEST_DIR = os.getenv(
        'STRUCTURED_AI_REMOTE_REQUEST_DIR',
        '/root/autodl-tmp/BUAA_SE_DetectFake/structured_test/',
    )
    REMOTE_COMMAND = os.getenv(
        'STRUCTURED_AI_REMOTE_COMMAND',
        'cd /root/autodl-tmp/BUAA_SE_DetectFake && /root/miniconda3/envs/llm/bin/python trigger_structured.py',
    )
    HOST = os.getenv('STRUCTURED_AI_HOST', 'connect.nmb1.seetacloud.com')
    PORT = int(os.getenv('STRUCTURED_AI_PORT', '24241'))
    USERNAME = os.getenv('STRUCTURED_AI_USERNAME', 'root')
    PASSWORD = os.getenv('STRUCTURED_AI_PASSWORD', '')
    READY_MARKER = os.getenv('STRUCTURED_AI_READY_MARKER', 'structured ready')
    RESULT_MARKER = os.getenv('STRUCTURED_AI_RESULT_MARKER', 'structured results')
    CONNECT_TIMEOUT = float(os.getenv('STRUCTURED_AI_CONNECT_TIMEOUT', '10'))
    READY_TIMEOUT = float(os.getenv('STRUCTURED_AI_READY_TIMEOUT', '60'))
    RESULT_TIMEOUT = float(os.getenv('STRUCTURED_AI_RESULT_TIMEOUT', '120'))
    SUBMIT_RETRY = int(os.getenv('STRUCTURED_AI_SUBMIT_RETRY', '2'))

    @staticmethod
    def _readline_with_timeout(stream, timeout_seconds: float):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if stream.channel.recv_ready():
                return stream.readline()
            if stream.channel.exit_status_ready():
                return ''
            time.sleep(0.1)
        raise StructuredAITransientError(f'read timeout after {timeout_seconds}s')

    @classmethod
    def _open_remote_session(cls):
        logger.info(
            'structured_ai connect host=%s port=%s user=%s command=%s request_dir=%s',
            cls.HOST,
            cls.PORT,
            cls.USERNAME,
            cls.REMOTE_COMMAND,
            cls.REMOTE_REQUEST_DIR,
        )
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                hostname=cls.HOST,
                username=cls.USERNAME,
                port=cls.PORT,
                password=cls.PASSWORD,
                timeout=cls.CONNECT_TIMEOUT,
                banner_timeout=cls.CONNECT_TIMEOUT,
                auth_timeout=cls.CONNECT_TIMEOUT,
            )
        except (paramiko.SSHException, OSError, TimeoutError) as exc:
            raise StructuredAITransientError(f'failed to connect structured AI host: {exc}') from exc

        try:
            stdin, stdout, stderr = ssh.exec_command(cls.REMOTE_COMMAND)
        except (paramiko.SSHException, OSError) as exc:
            ssh.close()
            raise StructuredAITransientError(f'failed to execute remote structured command: {exc}') from exc
        ready = False

        try:
            while True:
                line = cls._readline_with_timeout(stdout, cls.READY_TIMEOUT)
                if not line:
                    break
                if cls.READY_MARKER in line.strip().lower():
                    ready = True
                    break
        except StructuredAITransientError:
            ssh.close()
            raise

        if not ready:
            error_message = stderr.read().decode()
            ssh.close()
            raise StructuredAIPermanentError(error_message or 'Structured AI service did not become ready')

        return ssh, stdout, stderr

    @classmethod
    def _upload_request(cls, ssh, request_payload):
        temp_dir = tempfile.mkdtemp(prefix='structured-ai-')
        local_request_path = os.path.join(temp_dir, 'request.json')

        with open(local_request_path, 'w', encoding='utf-8') as handle:
            json.dump(request_payload, handle, ensure_ascii=False, indent=2)

        try:
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(local_request_path, cls.REMOTE_REQUEST_DIR)
            logger.info(
                'structured_ai uploaded request local=%s remote=%s',
                local_request_path,
                os.path.join(cls.REMOTE_REQUEST_DIR, 'request.json'),
            )
        except Exception as exc:
            raise StructuredAITransientError(f'failed to upload structured request: {exc}') from exc

        return temp_dir

    @classmethod
    def _read_result(cls, stdout, stderr):
        marker_found = False
        while True:
            line = cls._readline_with_timeout(stdout, cls.RESULT_TIMEOUT)
            if not line:
                break
            if cls.RESULT_MARKER in line.strip().lower():
                marker_found = True
                break

        if not marker_found:
            error_message = stderr.read().decode()
            raise StructuredAIPermanentError(error_message or 'Structured AI service returned no result marker')

        payload_line = cls._readline_with_timeout(stdout, cls.RESULT_TIMEOUT)
        if not payload_line:
            error_message = stderr.read().decode()
            raise StructuredAIPermanentError(error_message or 'Structured AI service returned empty payload')

        try:
            result_bytes = base64.b64decode(payload_line.strip())
            return json.loads(result_bytes.decode('utf-8'))
        except (ValueError, json.JSONDecodeError) as exc:
            raise StructuredAIPermanentError(f'invalid structured AI payload: {exc}') from exc

    @classmethod
    def submit(cls, request_payload):
        last_exc = None
        attempts = max(1, cls.SUBMIT_RETRY + 1)

        for attempt in range(1, attempts + 1):
            ssh = None
            temp_dir = None
            try:
                ssh, stdout, stderr = cls._open_remote_session()
                temp_dir = cls._upload_request(ssh, request_payload)
                return cls._read_result(stdout, stderr)
            except StructuredAITransientError as exc:
                last_exc = exc
                if attempt >= attempts:
                    break
            finally:
                if temp_dir and os.path.isdir(temp_dir):
                    for file_name in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, file_name))
                    os.rmdir(temp_dir)
                if ssh:
                    ssh.close()

        if last_exc:
            raise last_exc
        raise StructuredAITransientError('structured submit failed for unknown transient reason')
