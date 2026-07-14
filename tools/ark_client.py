from typing import Any

import requests


DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"


class ArkApiError(Exception):
    pass


def normalize_base_url(base_url: str | None) -> str:
    return (base_url or DEFAULT_BASE_URL).rstrip("/")


def get_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def request_json(
    method: str,
    url: str,
    *,
    api_key: str,
    timeout: int = 60,
    **kwargs: Any,
) -> dict[str, Any]:
    response = requests.request(
        method,
        url,
        headers=get_headers(api_key),
        timeout=timeout,
        **kwargs,
    )
    if response.status_code >= 400:
        raise ArkApiError(
            f"Ark API request failed: HTTP {response.status_code}, {response.text}"
        )
    try:
        return response.json()
    except ValueError as exc:
        raise ArkApiError("Ark API returned a non-JSON response") from exc


def list_models(api_key: str, base_url: str | None) -> list[dict[str, Any]]:
    payload = request_json(
        "GET",
        f"{normalize_base_url(base_url)}/models",
        api_key=api_key,
        timeout=30,
    )
    data = payload.get("data", [])
    if not isinstance(data, list):
        raise ArkApiError("Ark /models response does not contain a model list")
    return [model for model in data if isinstance(model, dict)]

