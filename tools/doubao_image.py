import base64
import time
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.ark_client import (
    ArkApiError,
    DEFAULT_BASE_URL,
    normalize_base_url,
    request_json,
)

VIDEO_MODEL_IDS = {
    "doubao-seedance-2-0-260128",
    "doubao-seedance-2-0-fast-260128",
    "doubao-seedance-2-0-mini-260615",
}

DEFAULT_MODEL = "doubao-seedream-4-0-250828"
DEFAULT_RESPONSE_FORMAT = "url"
DEFAULT_VIDEO_RATIO = "16:9"
DEFAULT_VIDEO_DURATION = "10"


class DoubaoImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials.get("api_key")
        if not api_key:
            yield self.create_text_message("Configure the Volcengine Ark API key in the plugin provider settings first.")
            return

        model = str(tool_parameters.get("model") or self.runtime.credentials.get("model") or DEFAULT_MODEL).strip()

        prompt = str(tool_parameters.get("prompt") or "").strip()
        if not prompt:
            yield self.create_text_message("Enter a prompt for image or video generation.")
            return

        try:
            base_url = normalize_base_url(DEFAULT_BASE_URL)
            if model in VIDEO_MODEL_IDS:
                yield from self._invoke_video(api_key, base_url, model, prompt, tool_parameters)
                return

            yield from self._invoke_image(api_key, base_url, model, prompt, tool_parameters)
        except (ArkApiError, requests.RequestException, ValueError) as exc:
            message = str(exc)
            if "InvalidEndpointOrModel.NotFound" in message:
                message += "\nVerify that the model parameter is the actual API model ID, not a display name."
            yield self.create_text_message(f"Doubao generation request failed: {message}")

    def _invoke_image(
        self,
        api_key: str,
        base_url: str,
        model: str,
        prompt: str,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage]:
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": tool_parameters.get("response_format") or DEFAULT_RESPONSE_FORMAT,
            "n": 1,
        }
        data = request_json(
            "POST",
            f"{base_url}/images/generations",
            api_key=api_key,
            json=payload,
            timeout=120,
        )
        images = data.get("data") or []
        if not images:
            raise ArkApiError("Ark response does not contain generated images")

        generated = []
        for image in images:
            if not isinstance(image, dict):
                continue
            if image.get("b64_json"):
                image_bytes = base64.b64decode(image["b64_json"])
                yield self.create_blob_message(
                    blob=image_bytes,
                    meta={"mime_type": "image/png"},
                )
                generated.append({"type": "b64_json", "mime_type": "image/png"})
            elif image.get("url"):
                url = image["url"]
                yield self.create_text_message(url)
                generated.append({"type": "url", "url": url})

        if not generated:
            raise ArkApiError("Ark response images do not contain b64_json or url")

        yield self.create_json_message(
            {
                "type": "image",
                "model": model,
                "prompt": prompt,
                "images": generated,
            }
        )

    def _invoke_video(
        self,
        api_key: str,
        base_url: str,
        model: str,
        prompt: str,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage]:
        ratio = str(tool_parameters.get("ratio") or DEFAULT_VIDEO_RATIO)
        duration = str(tool_parameters.get("duration") or DEFAULT_VIDEO_DURATION)
        video_prompt = prompt
        if ratio and "--ratio" not in video_prompt:
            video_prompt = f"{video_prompt} --ratio {ratio}"
        if duration and "--duration" not in video_prompt and "--dur" not in video_prompt:
            video_prompt = f"{video_prompt} --duration {duration}"

        task = request_json(
            "POST",
            f"{base_url}/contents/generations/tasks",
            api_key=api_key,
            json={
                "model": model,
                "content": [{"type": "text", "text": video_prompt}],
            },
            timeout=60,
        )
        task_id = task.get("id")
        if not task_id:
            raise ArkApiError("Ark response does not contain video generation task id")

        yield self.create_text_message(f"Video generation task created. Task ID: {task_id}")

        for attempt in range(60):
            time.sleep(5)
            task_data = request_json(
                "GET",
                f"{base_url}/contents/generations/tasks/{task_id}",
                api_key=api_key,
                timeout=60,
            )
            status = task_data.get("status")
            if status == "succeeded":
                video_url = _find_video_url(task_data)
                if not video_url:
                    raise ArkApiError("Ark video task succeeded but no video URL was returned")
                yield self.create_text_message(f"Video URL: {video_url}")
                yield self.create_json_message(
                    {
                        "type": "video",
                        "model": model,
                        "prompt": prompt,
                        "video_prompt": video_prompt,
                        "ratio": ratio,
                        "duration": duration,
                        "task_id": task_id,
                        "url": video_url,
                    }
                )
                return
            if status == "failed":
                error_message = (task_data.get("error") or {}).get("message") or "Unknown error"
                raise ArkApiError(f"Video generation task failed: {error_message}")
            if status == "canceled":
                raise ArkApiError("Video generation task was canceled")

            if attempt in {0, 5, 11, 23, 35, 47}:
                yield self.create_text_message(f"Video generation is still running. Waited {(attempt + 1) * 5} seconds...")

        raise ArkApiError("Video generation task timed out")


def _find_video_url(value: Any) -> str | None:
    if isinstance(value, dict):
        for key in ("video_url", "url"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.startswith(("http://", "https://")):
                return candidate
        for item in value.values():
            found = _find_video_url(item)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = _find_video_url(item)
            if found:
                return found
    return None
