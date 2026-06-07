import requests
from typing import List, Dict, Any
from .base_service import BaseService


class HIBPService(BaseService):
    _BASE_URL = "https://haveibeenpwned.com/api/v3/breaches"

    def check_domain_breaches(self, domain: str) -> List[Dict[str, Any]]:
        """Check confirmed data breaches for a given company domain."""
        response = requests.get(self._BASE_URL, params={"domain": domain}, timeout=10)
        response.raise_for_status()
        return [
            {
                "name": breach.get("Name"),
                "breach_date": breach.get("BreachDate"),
                "pwn_count": breach.get("PwnCount"),
                "data_classes": breach.get("DataClasses", []),
                "description": breach.get("Description"),
                "is_verified": breach.get("IsVerified"),
            }
            for breach in response.json()
        ]
    