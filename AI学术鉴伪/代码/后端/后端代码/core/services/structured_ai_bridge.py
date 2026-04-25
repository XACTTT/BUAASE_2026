import base64
import json
import os
import tempfile

import paramiko
from scp import SCPClient


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

    @classmethod
    def _open_remote_session(cls):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=cls.HOST,
            username=cls.USERNAME,
            port=cls.PORT,
            password=cls.PASSWORD,
        )

        stdin, stdout, stderr = ssh.exec_command(cls.REMOTE_COMMAND)
        ready = False

        while True:
            line = stdout.readline()
            if not line:
                break
            if cls.READY_MARKER in line.strip().lower():
                ready = True
                break

        if not ready:
            error_message = stderr.read().decode()
            ssh.close()
            raise RuntimeError(error_message or 'Structured AI service did not become ready')

        return ssh, stdout, stderr

    @classmethod
    def _upload_request(cls, ssh, request_payload):
        temp_dir = tempfile.mkdtemp(prefix='structured-ai-')
        local_request_path = os.path.join(temp_dir, 'request.json')

        with open(local_request_path, 'w', encoding='utf-8') as handle:
            json.dump(request_payload, handle, ensure_ascii=False, indent=2)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_request_path, cls.REMOTE_REQUEST_DIR)

        return temp_dir

    @classmethod
    def _read_result(cls, stdout, stderr):
        while True:
            line = stdout.readline()
            if not line:
                break
            if cls.RESULT_MARKER in line.strip().lower():
                break
        else:
            error_message = stderr.read().decode()
            raise RuntimeError(error_message or 'Structured AI service returned no result marker')

        payload_line = stdout.readline()
        if not payload_line:
            error_message = stderr.read().decode()
            raise RuntimeError(error_message or 'Structured AI service returned empty payload')

        result_bytes = base64.b64decode(payload_line.strip())
        return json.loads(result_bytes.decode('utf-8'))

    @classmethod
    def submit(cls, request_payload):
        ssh, stdout, stderr = cls._open_remote_session()
        temp_dir = None
        try:
            temp_dir = cls._upload_request(ssh, request_payload)
            return cls._read_result(stdout, stderr)
        finally:
            if temp_dir and os.path.isdir(temp_dir):
                for file_name in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file_name))
                os.rmdir(temp_dir)
            ssh.close()
