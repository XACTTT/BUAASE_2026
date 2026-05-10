import base64
import json
import os
import selectors
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import paramiko
from scp import SCPClient

from core.call_figure_detection import get_unified_ai_defaults


class BertTextAIError(RuntimeError):
    pass


class BertTextAITransientError(BertTextAIError):
    pass


class BertTextAIPermanentError(BertTextAIError):
    pass


class BertTextAIDetectionBridge:
    @staticmethod
    def _config():
        defaults = get_unified_ai_defaults()
        service_root = os.getenv(
            "UNIFIED_AI_SERVICE_ROOT",
            defaults["service_root"],
        )
        return {
            "mode": os.getenv("BERT_TEXT_AI_MODE", "local").strip().lower(),
            "service_root": service_root,
            "request_filename": "request.json",
            "ready_marker": os.getenv("UNIFIED_AI_READY_MARKER", defaults["ready_marker"]),
            "result_marker": os.getenv("UNIFIED_AI_RESULT_MARKER", defaults["result_marker"]),
            "connect_timeout": float(os.getenv("BERT_TEXT_AI_CONNECT_TIMEOUT", "10")),
            "ready_timeout": float(os.getenv("BERT_TEXT_AI_READY_TIMEOUT", "60")),
            "result_timeout": float(os.getenv("BERT_TEXT_AI_RESULT_TIMEOUT", "300")),
            "submit_retry": int(os.getenv("BERT_TEXT_AI_SUBMIT_RETRY", "1")),
            "host": os.getenv("BERT_TEXT_AI_HOST", defaults["host"]),
            "port": int(os.getenv("BERT_TEXT_AI_PORT", str(defaults["port"]))),
            "username": os.getenv("BERT_TEXT_AI_USERNAME", defaults["username"]),
            "password": os.getenv("BERT_TEXT_AI_PASSWORD", defaults["password"]),
            "remote_request_dir": os.getenv(
                "BERT_TEXT_AI_REMOTE_REQUEST_DIR",
                defaults["request_dir"],
            ),
            "remote_command": os.getenv(
                "BERT_TEXT_AI_REMOTE_COMMAND",
                defaults["command"],
            ),
            "local_python": os.getenv("UNIFIED_AI_PYTHON", defaults["python"]),
            "bert_project_root": os.getenv(
                "BERT_PROJECT_ROOT",
                "/mnt/data14/ccy/Bert/SE/AI_service/checkpoints",
            ),
            "bert_text_model_dir": os.getenv("BERT_TEXT_MODEL_DIR", ""),
        }

    @staticmethod
    def _build_request_payload(text: str, language: str | None = None, max_length: int | None = None):
        payload = {
            "request_id": f"bert-text-{int(time.time() * 1000)}",
            "pipeline": "bert",
            "payload": {
                "lang": BertTextAIDetectionBridge._normalize_language(language),
                "text": text,
            },
        }
        if max_length:
            payload["payload"]["max_length"] = int(max_length)
        return payload

    @staticmethod
    def _normalize_language(language: str | None) -> str:
        raw = (language or "").strip().lower()
        if raw in {"zh", "zh-cn", "zh_hans", "chinese", "cn"}:
            return "chinese"
        if raw:
            return raw
        return "chinese"

    @staticmethod
    def _resolve_local_python(config) -> str:
        if config["local_python"]:
            return config["local_python"]

        service_root = Path(config["service_root"])
        venv_python = service_root / ".venv" / "bin" / "python"
        if venv_python.is_file():
            return str(venv_python)
        return sys.executable

    @staticmethod
    def _read_local_line_with_timeout(proc: subprocess.Popen, selector: selectors.BaseSelector, timeout_seconds: float):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            events = selector.select(timeout=0.2)
            if events:
                line = proc.stdout.readline()
                if line:
                    return line
                if proc.poll() is not None:
                    break
            elif proc.poll() is not None:
                remaining = proc.stdout.readline()
                if remaining:
                    return remaining
                break
        raise BertTextAITransientError(f"read timeout after {timeout_seconds}s")

    @classmethod
    def _submit_local(cls, request_payload, config):
        service_root = Path(config["service_root"]).expanduser().resolve()
        trigger_path = service_root / "trigger_unified.py"
        if not trigger_path.is_file():
            raise BertTextAIPermanentError(f"unified ai entrypoint not found: {trigger_path}")

        temp_dir = tempfile.mkdtemp(prefix="bert-text-ai-")
        request_path = Path(temp_dir) / config["request_filename"]
        with request_path.open("w", encoding="utf-8") as handle:
            json.dump(request_payload, handle, ensure_ascii=False, indent=2)

        env = os.environ.copy()
        env["UNIFIED_AI_REQUEST_FILE"] = str(request_path)
        env.setdefault("BERT_PROJECT_ROOT", config["bert_project_root"])
        if config["bert_text_model_dir"]:
            env.setdefault("BERT_TEXT_MODEL_DIR", config["bert_text_model_dir"])

        proc = None
        selector = None
        try:
            proc = subprocess.Popen(
                [cls._resolve_local_python(config), str(trigger_path)],
                cwd=str(service_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            if proc.stdout is None:
                raise BertTextAITransientError("failed to open unified AI stdout pipe")

            selector = selectors.DefaultSelector()
            selector.register(proc.stdout, selectors.EVENT_READ)

            ready_seen = False
            while True:
                line = cls._read_local_line_with_timeout(proc, selector, config["ready_timeout"])
                if config["ready_marker"] in line.strip().lower():
                    ready_seen = True
                    break

            if not ready_seen:
                raise BertTextAIPermanentError("unified AI service did not become ready")

            marker_seen = False
            while True:
                line = cls._read_local_line_with_timeout(proc, selector, config["result_timeout"])
                if config["result_marker"] in line.strip().lower():
                    marker_seen = True
                    break

            if not marker_seen:
                raise BertTextAIPermanentError("unified AI service returned no result marker")

            payload_line = cls._read_local_line_with_timeout(proc, selector, config["result_timeout"]).strip()
            return cls._decode_outer_payload(payload_line)
        finally:
            if selector is not None:
                selector.close()
            if proc is not None and proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)
            try:
                request_path.unlink(missing_ok=True)
                Path(temp_dir).rmdir()
            except OSError:
                pass

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
            raise BertTextAITransientError(f"failed to connect unified AI host: {exc}") from exc

        try:
            stdin, stdout, stderr = ssh.exec_command(config["remote_command"])
        except (paramiko.SSHException, OSError) as exc:
            ssh.close()
            raise BertTextAITransientError(f"failed to execute unified AI command: {exc}") from exc

        ready = False
        while True:
            line = cls._read_remote_line_with_timeout(stdout, config["ready_timeout"])
            if not line:
                break
            if config["ready_marker"] in line.strip().lower():
                ready = True
                break

        if not ready:
            error_message = stderr.read().decode()
            ssh.close()
            raise BertTextAIPermanentError(error_message or "unified AI service did not become ready")

        return ssh, stdout, stderr

    @staticmethod
    def _read_remote_line_with_timeout(stream, timeout_seconds: float):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            if stream.channel.recv_ready():
                return stream.readline()
            if stream.channel.exit_status_ready():
                return stream.readline()
            time.sleep(0.1)
        raise BertTextAITransientError(f"read timeout after {timeout_seconds}s")

    @classmethod
    def _submit_remote(cls, request_payload, config):
        ssh = None
        stdout = None
        stderr = None
        temp_dir = tempfile.mkdtemp(prefix="bert-text-ai-")
        local_request_path = Path(temp_dir) / config["request_filename"]
        with local_request_path.open("w", encoding="utf-8") as handle:
            json.dump(request_payload, handle, ensure_ascii=False, indent=2)

        try:
            ssh, stdout, stderr = cls._open_remote_session(config)
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(str(local_request_path), config["remote_request_dir"])

            marker_found = False
            while True:
                line = cls._read_remote_line_with_timeout(stdout, config["result_timeout"])
                if not line:
                    break
                if config["result_marker"] in line.strip().lower():
                    marker_found = True
                    break

            if not marker_found:
                error_message = stderr.read().decode()
                raise BertTextAIPermanentError(error_message or "unified AI service returned no result marker")

            payload_line = cls._read_remote_line_with_timeout(stdout, config["result_timeout"]).strip()
            return cls._decode_outer_payload(payload_line)
        finally:
            try:
                local_request_path.unlink(missing_ok=True)
                Path(temp_dir).rmdir()
            except OSError:
                pass
            if ssh:
                ssh.close()

    @staticmethod
    def _decode_outer_payload(payload_line: str):
        if not payload_line:
            raise BertTextAIPermanentError("unified AI service returned empty payload")

        try:
            decoded = json.loads(base64.b64decode(payload_line).decode("utf-8"))
        except (ValueError, json.JSONDecodeError) as exc:
            raise BertTextAIPermanentError(f"invalid unified AI payload: {exc}") from exc

        if not decoded.get("success", False):
            error = decoded.get("error") or {}
            message = error.get("message") or "bert text detection failed"
            raise BertTextAIPermanentError(message)

        result = decoded.get("result")
        if not isinstance(result, dict):
            raise BertTextAIPermanentError("bert text result payload must be an object")
        return result

    @classmethod
    def submit_text(cls, text: str, language: str | None = None, max_length: int | None = None):
        request_payload = cls._build_request_payload(text=text, language=language, max_length=max_length)
        config = cls._config()
        last_exc = None
        attempts = max(1, config["submit_retry"] + 1)

        for attempt in range(1, attempts + 1):
            try:
                if config["mode"] == "ssh":
                    return cls._submit_remote(request_payload, config)
                return cls._submit_local(request_payload, config)
            except BertTextAITransientError as exc:
                last_exc = exc
                if attempt >= attempts:
                    break

        if last_exc:
            raise last_exc
        raise BertTextAITransientError("bert text submit failed for unknown transient reason")
