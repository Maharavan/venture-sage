from strands import tool
from typing import List, Dict, Any
from services.exa_service import ExaService
from services.hibp_service import HIBPService


@tool
def search_security_incidents_tool(companies: List[str], domains: List[str]) -> Dict[str, Any]:
    """
    Search for security incidents including data breaches (via HIBP),
    CVEs, outages, and vulnerability disclosures for each company.
    companies and domains must be in the same order.
    """
    try:
        exa = ExaService()
        hibp = HIBPService()
        results = {}
        for company, domain in zip(companies, domains):
            query = f"{company} security breach data leak CVE vulnerability incident outage"
            results[company] = {
                "breaches": hibp.check_domain_breaches(domain),
                "security_incidents": exa.search_and_contents(query),
            }
        return {"status": "success", "company_count": len(companies), "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
