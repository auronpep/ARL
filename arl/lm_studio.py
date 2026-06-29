from __future__ import annotations

import json
import urllib.error
import urllib.request


def normalize_base_url(base_url: str) -> str:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/v1"):
        return base_url[:-3]
    return base_url


def request_json(url: str, payload: dict | None = None, timeout_sec: int = 600) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout_sec) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LM Studio HTTP {error.code}: {body}") from error


def resolve_model(base_url: str, requested_model: str | None, timeout_sec: int = 600) -> str:
    if requested_model:
        return requested_model
    models = request_json(f"{base_url}/v1/models", timeout_sec=timeout_sec)
    loaded = models.get("data", [])
    if not loaded:
        raise RuntimeError("LM Studio has no loaded models. Load one in LM Studio, then retry.")
    # ponytail: first loaded model is enough for this local one-model workflow.
    return loaded[0]["id"]


def chat(prompt: str, base_url: str, model: str | None = None, max_tokens: int = 4096, timeout_sec: int = 600) -> tuple[str, str]:
    base_url = normalize_base_url(base_url)
    model = resolve_model(base_url, model, timeout_sec)
    response = request_json(
        f"{base_url}/v1/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": max_tokens,
            "stream": False,
        },
        timeout_sec=timeout_sec,
    )
    return response["choices"][0]["message"].get("content", ""), model

