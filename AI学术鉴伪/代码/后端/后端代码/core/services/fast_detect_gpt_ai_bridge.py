import base64
import json
import os
import tempfile
import time
from pathlib import Path

import paramiko
from scp import SCPClient

from core.call_figure_detection import get_unified_ai_defaults


class FastDetectGPTAIError(RuntimeError):
    pass


class FastDetectGPTAITransientError(FastDetectGPTAIError):
    pass


class FastDetectGPTAIPermanentError(FastDetectGPTAIError):
    pass


class FastDetectGPTAIDetectionBridge:
    @staticmethod
    def _config():
        defaults = get_unified_ai_defaults()
        return {
            "mode": os.getenv("FAST_DETECT_GPT_AI_MODE", "auto").strip().lower(),
            "service_root": os.getenv("FAST_DETECT_GPT_AI_SERVICE_ROOT", defaults["service_root"]),
            "request_filename": "request.json",
            "ready_marker": os.getenv("UNIFIED_AI_READY_MARKER", defaults["ready_marker"]),
            "result_marker": os.getenv("UNIFIED_AI_RESULT_MARKER", defaults["result_marker"]),
            "connect_timeout": float(os.getenv("FAST_DETECT_GPT_AI_CONNECT_TIMEOUT", "10")),
            "ready_timeout": float(os.getenv("FAST_DETECT_GPT_AI_READY_TIMEOUT", "60")),
            "result_timeout": float(os.getenv("FAST_DETECT_GPT_AI_RESULT_TIMEOUT", "300")),
            "submit_retry": int(os.getenv("FAST_DETECT_GPT_AI_SUBMIT_RETRY", "1")),
            "host": os.getenv("FAST_DETECT_GPT_AI_HOST", defaults["host"]),
            "port": int(os.getenv("FAST_DETECT_GPT_AI_PORT", str(defaults["port"]))),
            "username": os.getenv("FAST_DETECT_GPT_AI_USERNAME", defaults["username"]),
            "password": os.getenv("FAST_DETECT_GPT_AI_PASSWORD", defaults["password"]),
            "remote_request_dir": os.getenv("FAST_DETECT_GPT_AI_REMOTE_REQUEST_DIR", defaults["request_dir"]),
            "remote_command": os.getenv("FAST_DETECT_GPT_AI_REMOTE_COMMAND", defaults["command"]),
            "local_python": os.getenv("UNIFIED_AI_PYTHON", defaults["python"]),
            "project_root": os.getenv("FAST_DETECT_GPT_PROJECT_ROOT", ""),
            "model_name": os.getenv("FAST_DETECT_GPT_MODEL_NAME", "falcon-7b"),
            "max_length": int(os.getenv("FAST_DETECT_GPT_MAX_LENGTH", "256")),
            "load_in_8bit": os.getenv("FAST_DETECT_GPT_LOAD_IN_8BIT", "false").strip().lower() == "true",
            "load_in_4bit": os.getenv("FAST_DETECT_GPT_LOAD_IN_4BIT", "false").strip().lower() == "true",
        }

    @staticmethod
    def _build_request_payload(text: str, question: str | None = None, max_length: int | None = None):
        payload = {
            "request_id": f"fast-detect-gpt-{int(time.time() * 1000)}",
            "pipeline": "fast_detect_gpt",
            "payload": {
                "text": text,
            },
        }
        if question:
            payload["payload"]["question"] = question
        if max_length is not None:
            payload["payload"]["max_length"] = int(max_length)
        return payload

    @staticmethod
    def _readline_with_timeout(stream, timeout_seconds: float):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if stream.channel.recv_ready():
                return stream.readline()
            if stream.channel.exit_status_ready():
                return stream.readline()
            time.sleep(0.1)
        raise FastDetectGPTAITransientError(f"read timeout after {timeout_seconds}s")

    @classmethod
    def _open_remote_session(cls, config):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                hostname=config["host"],
                username=config["username"],
                port=config["port"],
                password=config["password"],
                timeout=config["connect_timeout"],
                banner_timeout=config["connect_timeout"],
                auth_timeout=config["connect_timeout"],
            )
        except (paramiko.SSHException, OSError, TimeoutError) as exc:
            raise FastDetectGPTAITransientError(f"failed to connect fast_detect_gpt host: {exc}") from exc

        try:
            stdin, stdout, stderr = ssh.exec_command(config["remote_command"])
        except (paramiko.SSHException, OSError) as exc:
            ssh.close()
            raise FastDetectGPTAITransientError(f"failed to execute fast_detect_gpt remote command: {exc}") from exc

        ready = False
        while True:
            line = cls._readline_with_timeout(stdout, config["ready_timeout"])
            if not line:
                break
            if config["ready_marker"] in line.strip().lower():
                ready = True
                break

        if not ready:
            error_message = stderr.read().decode()
            ssh.close()
            raise FastDetectGPTAIPermanentError(error_message or "fast_detect_gpt service did not become ready")

        return ssh, stdout, stderr

    @classmethod
    def _submit_remote(cls, request_payload, config):
        ssh = None
        temp_dir = tempfile.mkdtemp(prefix="fast-detect-gpt-ai-")
        local_request_path = Path(temp_dir) / config["request_filename"]
        with local_request_path.open("w", encoding="utf-8") as handle:
            json.dump(request_payload, handle, ensure_ascii=False, indent=2)

        try:
            ssh, stdout, stderr = cls._open_remote_session(config)
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(str(local_request_path), config["remote_request_dir"])

            marker_found = False
            while True:
                line = cls._readline_with_timeout(stdout, config["result_timeout"])
                if not line:
                    break
                if config["result_marker"] in line.strip().lower():
                    marker_found = True
                    break

            if not marker_found:
                error_message = stderr.read().decode()
                raise FastDetectGPTAIPermanentError(
                    error_message or "fast_detect_gpt service returned no result marker"
                )

            payload_line = cls._readline_with_timeout(stdout, config["result_timeout"]).strip()
            if not payload_line:
                raise FastDetectGPTAIPermanentError("fast_detect_gpt service returned empty payload")

            decoded = json.loads(base64.b64decode(payload_line).decode("utf-8"))
            if not decoded.get("success", False):
                error = decoded.get("error") or {}
                message = error.get("message") or "fast_detect_gpt failed"
                raise FastDetectGPTAIPermanentError(message)

            result = decoded.get("result")
            if not isinstance(result, dict):
                raise FastDetectGPTAIPermanentError("fast_detect_gpt result payload must be an object")
            return result
        finally:
            try:
                local_request_path.unlink(missing_ok=True)
                Path(temp_dir).rmdir()
            except OSError:
                pass
            if ssh:
                ssh.close()

    @classmethod
    def submit_text(cls, text: str, question: str | None = None, max_length: int | None = None):
        config = cls._config()
        request_payload = cls._build_request_payload(
            text=text,
            question=question,
            max_length=max_length or config["max_length"],
        )

        last_exc = None
        attempts = max(1, config["submit_retry"] + 1)
        mode = config["mode"]

        for attempt in range(1, attempts + 1):
            try:
                if mode == "ssh":
                    return cls._submit_remote(request_payload, config)
                if mode == "auto":
                    return cls._submit_remote(request_payload, config)
                return cls._submit_remote(request_payload, config)
            except FastDetectGPTAITransientError as exc:
                last_exc = exc
                if attempt >= attempts:
                    break

        if last_exc:
            raise last_exc
        raise FastDetectGPTAITransientError("fast_detect_gpt submit failed for unknown transient reason")
