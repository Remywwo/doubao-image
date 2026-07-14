from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.ark_client import ArkApiError, DEFAULT_BASE_URL, list_models


class DoubaoImageProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = str(credentials.get("api_key") or "").strip()
        if not api_key:
            raise ToolProviderCredentialValidationError("API Key is required")

        try:
            list_models(api_key, DEFAULT_BASE_URL)
        except ArkApiError as e:
            raise ToolProviderCredentialValidationError(str(e))
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"Credential validation failed: {e}")
