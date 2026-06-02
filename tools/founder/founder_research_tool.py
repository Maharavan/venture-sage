from strands import tool
from typing import List, Dict, Any
from services.exa_service import ExaService


@tool
def get_founder_background(founders: List[str]) -> Dict[str, Any]:
    """Extract the founder's background information from the provided description."""
    try:
        exa = ExaService()
        result = {}
        for founder in founders:
            query = f"{founder} biography experience startup founder"
            result[founder] = exa.search(query)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
