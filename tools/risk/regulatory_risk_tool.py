from strands import tool
from typing import List, Dict, Any
from services.exa_service import ExaService


@tool
def search_regulatory_risk_tool(companies: List[str]) -> Dict[str, Any]:
    """
    Search for regulatory risks including lawsuits, fines, compliance violations,
    GDPR/CCPA issues, and government investigations associated with a company.
    """
    try:
        exa = ExaService()
        results = {}
        for company in companies:
            query = f"{company} regulatory compliance GDPR CCPA data privacy government policy legal"
            results[company] = exa.search_and_contents(query, max_text_length=600)
        return {"status": "success", "company_count": len(companies), "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
