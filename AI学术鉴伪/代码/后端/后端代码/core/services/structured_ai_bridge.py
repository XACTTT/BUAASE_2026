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
    @staticmethod
    def _config():
        return {
            'remote_root': os.getenv('STRUCTURED_AI_REMOTE_ROOT', '/root/autodl-tmp/BUAA_SE_DetectFake'),
            'remote_request_dir': os.getenv(
                'STRUCTURED_AI_REMOTE_REQUEST_DIR',
                '/root/autodl-tmp/BUAA_SE_DetectFake/structured_test/',
            ),
            'remote_command': os.getenv(
                'STRUCTURED_AI_REMOTE_COMMAND',
                'cd /root/autodl-tmp/BUAA_SE_DetectFake && /root/miniconda3/envs/llm/bin/python trigger_structured.py',
            ),
            'host': os.getenv('STRUCTURED_AI_HOST', 'connect.nmb1.seetacloud.com'),
            'port': int(os.getenv('STRUCTURED_AI_PORT', '24241')),
            'username': os.getenv('STRUCTURED_AI_USERNAME', 'root'),
            'password': os.getenv('STRUCTURED_AI_PASSWORD', ''),
            'ready_marker': os.getenv('STRUCTURED_AI_READY_MARKER', 'structured ready'),
            'result_marker': os.getenv('STRUCTURED_AI_RESULT_MARKER', 'structured results'),
            'connect_timeout': float(os.getenv('STRUCTURED_AI_CONNECT_TIMEOUT', '10')),
            'ready_timeout': float(os.getenv('STRUCTURED_AI_READY_TIMEOUT', '60')),
            'result_timeout': float(os.getenv('STRUCTURED_AI_RESULT_TIMEOUT', '120')),
            'submit_retry': int(os.getenv('STRUCTURED_AI_SUBMIT_RETRY', '2')),
        }

    @staticmethod
    def _readline_with_timeout(stream, timeout_seconds: float):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if stream.channel.recv_ready():
                return stream.readline()
            if stream.channel.exit_status_ready():
                # Paramiko may already have prefetched the trailing stdout data into
                # the file-like wrapper even after the remote process exits. Read one
                # more line here so we do not drop the final payload line.
                return stream.readline()
            time.sleep(0.1)
        raise StructuredAITransientError(f'read timeout after {timeout_seconds}s')

    @classmethod
    def _open_remote_session(cls, config):
        logger.info(
            'structured_ai connect host=%s port=%s user=%s command=%s request_dir=%s',
            config['host'],
            config['port'],
            config['username'],
            config['remote_command'],
            config['remote_request_dir'],
        )
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                hostname=config['host'],
                username=config['username'],
                port=config['port'],
                password=config['password'],
                timeout=config['connect_timeout'],
                banner_timeout=config['connect_timeout'],
                auth_timeout=config['connect_timeout'],
            )
        except (paramiko.SSHException, OSError, TimeoutError) as exc:
            raise StructuredAITransientError(f'failed to connect structured AI host: {exc}') from exc

        try:
            stdin, stdout, stderr = ssh.exec_command(config['remote_command'])
        except (paramiko.SSHException, OSError) as exc:
            ssh.close()
            raise StructuredAITransientError(f'failed to execute remote structured command: {exc}') from exc
        ready = False

        try:
            while True:
                line = cls._readline_with_timeout(stdout, config['ready_timeout'])
                if not line:
                    break
                if config['ready_marker'] in line.strip().lower():
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
    def _upload_request(cls, ssh, request_payload, config):
        temp_dir = tempfile.mkdtemp(prefix='structured-ai-')
        local_request_path = os.path.join(temp_dir, 'request.json')

        with open(local_request_path, 'w', encoding='utf-8') as handle:
            json.dump(request_payload, handle, ensure_ascii=False, indent=2)

        try:
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(local_request_path, config['remote_request_dir'])
            logger.info(
                'structured_ai uploaded request local=%s remote=%s',
                local_request_path,
                os.path.join(config['remote_request_dir'], 'request.json'),
            )
        except Exception as exc:
            raise StructuredAITransientError(f'failed to upload structured request: {exc}') from exc

        return temp_dir

    @classmethod
    def _read_result(cls, stdout, stderr, config):
        marker_found = False
        while True:
            line = cls._readline_with_timeout(stdout, config['result_timeout'])
            if not line:
                break
            if config['result_marker'] in line.strip().lower():
                marker_found = True
                break

        if not marker_found:
            error_message = stderr.read().decode()
            raise StructuredAIPermanentError(error_message or 'Structured AI service returned no result marker')

        payload_line = cls._readline_with_timeout(stdout, config['result_timeout'])
        if not payload_line:
            # The remote process may exit immediately after printing the payload.
            # Drain any remaining buffered stdout before concluding that no payload
            # was returned.
            remaining = stdout.read()
            if isinstance(remaining, bytes):
                remaining = remaining.decode('utf-8', errors='ignore')
            if remaining:
                payload_line = remaining.splitlines()[0].strip()

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
        config = cls._config()
        last_exc = None
        attempts = max(1, config['submit_retry'] + 1)

        for attempt in range(1, attempts + 1):
            ssh = None
            temp_dir = None
            try:
                ssh, stdout, stderr = cls._open_remote_session(config)
                temp_dir = cls._upload_request(ssh, request_payload, config)
                return cls._read_result(stdout, stderr, config)
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
