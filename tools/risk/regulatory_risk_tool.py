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
            query = f"""
            {company} lawsuit regulatory fine compliance violation
            GDPR CCPA data privacy government investigation
            legal action penalty regulatory action
            """
            results[company] = exa.search_and_contents(query)
        return {"status": "success", "company_count": len(companies), "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
