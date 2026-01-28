"""Fetch the interview scorecard content."""

from typing import Dict, Any, List
from tools.common import (
    SCORECARD_DB_ID, 
    SCORECARD_DATA_SOURCE_ID, 
    SCORECARD_URL,
    query_database_complete
)


# Director of Product competency framework (hardcoded for reliability)
COMPETENCY_FRAMEWORK = {
    "builder_operator": [
        {
            "name": "⚙️ Execution / Org Process",
            "description": "Delivering outcomes AND building systems that enable repeatable delivery",
            "evidence_to_look_for": [
                "Shipping under pressure",
                "Creating operating rhythms",
                "Establishing predictability",
                "Both heroic delivery AND sustainable process creation"
            ]
        },
        {
            "name": "🌱 Org Building / People Management",
            "description": "Building teams and establishing operating models",
            "evidence_to_look_for": [
                "Hiring decisions",
                "Team composition",
                "Developing ICs",
                "Scaling organizations",
                "Building from scratch",
                "Bringing structure to chaos"
            ]
        },
        {
            "name": "🤝 Influence",
            "description": "Cross-functional leadership and stakeholder management",
            "evidence_to_look_for": [
                "Getting buy-in",
                "Navigating orgs",
                "Managing up/across",
                "Executive communication",
                "Influence without authority",
                "Building coalitions"
            ]
        }
    ],
    "product_leadership": [
        {
            "name": "🧭 Direction",
            "description": "Translating vision into strategy and roadmaps",
            "evidence_to_look_for": [
                "Strategic planning",
                "Prioritization frameworks",
                "Roadmap creation",
                "Vision-to-execution translation",
                "Strategic decision-making"
            ]
        },
        {
            "name": "💡 Insight",
            "description": "Customer understanding and market awareness",
            "evidence_to_look_for": [
                "Customer research",
                "Discovery processes",
                "Market analysis",
                "Deep qualitative understanding",
                "Insight-driven decisions"
            ]
        }
    ],
    "grading_scale": {
        "A+": "Exceptional evidence; exceeds expectations significantly",
        "A": "Strong evidence of excellence; exceeds expectations",
        "A-": "Good evidence of strength; slightly above expectations",
        "B+": "Solid evidence; meets expectations well",
        "B": "Adequate evidence; meets expectations",
        "B-": "Some evidence; meets expectations with notable gaps",
        "C+": "Limited evidence; below expectations",
        "C": "Minimal evidence; significant gaps",
        "C-": "Very limited or no evidence; major concerns"
    }
}


def fetch_scorecard() -> Dict[str, Any]:
    """Fetch the interview scorecard structure and candidate entries.
    
    The scorecard is stored as a Notion database. This function returns:
    - The competency framework (hardcoded for reliability)
    - Candidate entries from the database (if accessible)
    
    Returns:
        Dictionary containing:
        - framework: The 5-competency evaluation framework
        - candidates: List of candidate scorecard entries (if accessible)
        - database_url: URL to the scorecard database
    """
    result = {
        "framework": COMPETENCY_FRAMEWORK,
        "database_url": SCORECARD_URL,
        "database_id": SCORECARD_DB_ID,
        "data_source_id": SCORECARD_DATA_SOURCE_ID,
        "candidates": [],
        "error": None
    }
    
    try:
        # Query the database to get candidate entries
        pages = query_database_complete(
            database_id=SCORECARD_DATA_SOURCE_ID,
            use_data_source=True
        )
        
        # Extract candidate info from each page
        candidates = []
        for page in pages:
            props = page.get("properties", {})
            
            # Extract candidate name
            candidate_name = ""
            name_prop = props.get("Candidate", {})
            if name_prop.get("title"):
                candidate_name = "".join([item.get("plain_text", "") for item in name_prop["title"]])
            
            # Extract decision status
            decision = ""
            decision_prop = props.get("Decision", {})
            if decision_prop.get("status"):
                decision = decision_prop["status"].get("name", "")
            
            candidates.append({
                "page_id": page.get("id"),
                "name": candidate_name,
                "decision": decision,
                "properties": props
            })
        
        result["candidates"] = candidates
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


def get_competency_framework() -> Dict[str, Any]:
    """Get the competency framework without querying Notion.
    
    Use this when you just need the framework structure for analysis.
    
    Returns:
        The 5-competency evaluation framework
    """
    return COMPETENCY_FRAMEWORK
