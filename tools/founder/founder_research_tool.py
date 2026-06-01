from strands import tool
from exa_py import Exa
import os
from typing import List, Dict, Any
@tool
def get_founder_background(founders: List[str]) -> Dict[str, Any]:
    """Extract the founder's background information from the provided description."""

    try:
        api_key = os.getenv("EXA_API_KEY")
        if not api_key:
            return {
                "status": "error",
                "message": "EXA_API_KEY environment variable not set."
            }

        exa = Exa(api_key=api_key)
        result = {}
        for founder in founders:
            query = f"""
            {founder} biography experience startup founder
            """
            search_results = exa.search(query, num_results=5)
            result[founder] = [
                {
                    "title": r.title,
                    "url": r.url,
                    "text": r.text
                }
                for r in search_results.results
            ]

        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }