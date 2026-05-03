import json
from typing import Any, Dict
from urllib import error as url_error
from urllib import request as url_request


def build_chat_completion_payload(
    model: str,
    messages: list[dict],
    temperature: float,
    top_p: float,
    max_tokens: int,
    response_format: dict | None = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }
    if response_format:
        payload["response_format"] = response_format
    return payload


def call_openai_compatible_chat(
    base_url: str,
    api_key: str,
    payload: Dict[str, Any],
    timeout: int,
) -> Dict[str, Any]:
    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = url_request.Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with url_request.urlopen(req, timeout=timeout) as response:
            raw_body = response.read().decode("utf-8", errors="ignore")
    except url_error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="ignore")
        raise ValueError(raw_body or "Chat completion failed") from exc
    except url_error.URLError as exc:
        raise ConnectionError("Chat completion connection failed") from exc

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Chat completion returned invalid JSON") from exc
