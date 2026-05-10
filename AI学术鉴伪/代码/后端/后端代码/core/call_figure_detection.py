import atexit
import base64
import pickle
from pathlib import Path

import paramiko
from scp import SCPClient, SCPException


# ---------------------------------------------------------------------------
# Remote AI service configuration
# Edit this section when the remote server or command changes.
# ---------------------------------------------------------------------------
REMOTE_AI_CONFIG = {
    "connect_on_import": False,
    "hostname": "124.115.123.132",
    "port": 22214,
    "username": "ccy",
    "password": "chencanyu@a800@air",
    "remote_workdir": "/mnt/data14/ccy/Bert/SE/AI_service/service_code",
    "remote_python": "/mnt/data14/ccy/pip_packs/miniconda3/envs/bert/bin/python",
    "remote_entrypoint": "trigger_unified.py",
    "remote_ready_marker": "ai service ready",
    "remote_result_marker": "ai service result",
    "remote_upload_dir": "/mnt/data14/ccy/Bert/SE/AI_service/service_code/test/",
}


stdin = None
stdout = None
stderr = None
ssh = None


def build_remote_command(config: dict) -> str:
    return f"cd {config['remote_workdir']} && {config['remote_python']} {config['remote_entrypoint']}"


def get_unified_ai_defaults(config=None) -> dict:
    config = config or REMOTE_AI_CONFIG
    remote_workdir = Path(config["remote_workdir"])
    return {
        "service_root": str(remote_workdir),
        "request_dir": str(remote_workdir / "requests"),
        "command": build_remote_command(config),
        "python": config["remote_python"],
        "host": config["hostname"],
        "port": config["port"],
        "username": config["username"],
        "password": config["password"],
        "ready_marker": config["remote_ready_marker"],
        "result_marker": config["remote_result_marker"],
    }


def remote_call(hostname, username, port, password, config=None):
    config = config or REMOTE_AI_CONFIG

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, port=port, password=password)

    command = build_remote_command(config)
    stdin_stream, stdout_stream, stderr_stream = ssh_client.exec_command(command)

    success_detected = False
    while True:
        line = stdout_stream.readline()
        if not line:
            break
        line = line.strip()
        print("远程输出:", line)
        if config["remote_ready_marker"].lower() in line.lower():
            success_detected = True
            break

    if not success_detected:
        err = stderr_stream.read().decode()
        ssh_client.close()
        if err:
            raise RuntimeError(f"远程执行错误: {err}")
        raise RuntimeError(f"远程脚本未返回准备标记: {config['remote_ready_marker']}")

    return stdin_stream, stdout_stream, stderr_stream, ssh_client


def remote_monitor(stdout_stream, stderr_stream, config=None):
    config = config or REMOTE_AI_CONFIG
    result_detected = False
    while True:
        line = stdout_stream.readline()
        if not line:
            err = stderr_stream.read().decode()
            if err:
                raise RuntimeError(f"远程执行错误:{err}")
            break
        line = line.strip()
        print("远程输出:", line)
        if config["remote_result_marker"].lower() in line.lower():
            result_detected = True
            break

    if not result_detected:
        err = stderr_stream.read().decode()
        if err:
            raise RuntimeError(f"远程执行错误: {err}")
        raise RuntimeError(f"远程脚本未返回结果标记: {config['remote_result_marker']}")

    output = stdout_stream.readline()
    result_bytes = base64.b64decode(output)
    return pickle.loads(result_bytes)


def transfer_image(ssh_client, local_path, remote_path=None, config=None):
    config = config or REMOTE_AI_CONFIG
    remote_path = remote_path or config["remote_upload_dir"]
    try:
        with SCPClient(ssh_client.get_transport()) as scp:
            scp.put(str(local_path), remote_path)
            print(f"成功传输到: {remote_path}")
    except SCPException as exc:
        print(f"传输失败: {str(exc)}")
    except Exception as exc:
        print(f"发生错误: {str(exc)}")


def close_ssh_connection():
    global ssh
    try:
        if ssh:
            ssh.close()
            print("SSH 连接已关闭")
    except Exception as exc:
        print(f"关闭 SSH 连接时发生错误: {exc}")


atexit.register(close_ssh_connection)


def ensure_connection(config=None):
    global stdin, stdout, stderr, ssh
    config = config or REMOTE_AI_CONFIG
    if ssh is not None:
        return
    stdin, stdout, stderr, ssh = remote_call(
        config["hostname"],
        config["username"],
        config["port"],
        config["password"],
        config=config,
    )


def reconnect(config=None):
    global stdin, stdout, stderr, ssh
    config = config or REMOTE_AI_CONFIG
    if ssh is not None:
        ssh.close()
    stdin, stdout, stderr, ssh = remote_call(
        config["hostname"],
        config["username"],
        config["port"],
        config["password"],
        config=config,
    )


def get_result(local_path, json_path, config=None):
    global ssh, stdout, stderr
    config = config or REMOTE_AI_CONFIG
    ensure_connection(config)

    transfer_image(ssh, json_path, config=config)
    transfer_image(ssh, local_path, config=config)

    try:
        result = remote_monitor(stdout, stderr, config=config)
        print("远程调用结果:", result)
    except Exception as exc:
        print(f"发生错误: {str(exc)}")
        return None
    return result


if REMOTE_AI_CONFIG["connect_on_import"]:
    ensure_connection()


if __name__ == "__main__":
    ensure_connection()

    local_path = Path("img.zip")
    json_path = Path("data.json")
    transfer_image(ssh, json_path)
    transfer_image(ssh, local_path)

    try:
        result = remote_monitor(stdout, stderr)
        print("远程调用结果:", result)
        ssh.close()
    except Exception as exc:
        print(f"发生错误: {str(exc)}")
        result = None

    if result is not None:
        with open("result_new_llm.pkl", "wb") as file:
            pickle.dump(result, file)
