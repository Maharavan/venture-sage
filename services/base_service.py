import os
from typing import Any, Dict


class BaseService:
    def _require_env(self, name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise EnvironmentError(f"{name} environment variable is not set.")
        return value

    def error(self, message: str) -> Dict[str, Any]:
        return {"status": "error", "message": message}

    def success(self, **kwargs) -> Dict[str, Any]:
        return {"status": "success", **kwargs}
