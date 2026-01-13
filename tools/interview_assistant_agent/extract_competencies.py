"""Extract competency-related content from transcript."""

from typing import List, Dict, Any


def extract_competencies(transcript: str, competency_model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract competency-related content from transcript.
    
    Args:
        transcript: Interview transcript text
        competency_model: Notion page object containing competency model
    
    Returns:
        List of extracted competency evidence
    """
    # This is a placeholder - actual implementation would parse the competency model
    # and extract relevant sections from the transcript
    # For now, return structure for agent to fill in
    
    return [
        {
            "competency": "Placeholder",
            "evidence": [],
            "strengths": [],
            "gaps": []
        }
    ]
