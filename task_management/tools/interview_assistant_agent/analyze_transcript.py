"""Analyze interview transcript against scorecard criteria."""

from typing import Dict, Any, List, Optional
from tools.notion import get_transcript_content


def analyze_transcript(
    transcript_content: str,
    scorecard_content: str,
    candidate_name: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze an interview transcript against scorecard criteria.
    
    This tool structures the transcript and scorecard data for analysis.
    The agent's LLM will perform the actual analysis based on this structured data.
    
    Args:
        transcript_content: Full transcript text content
        scorecard_content: Scorecard criteria text/content from Notion page
        candidate_name: Optional candidate name for context
    
    Returns:
        Dictionary containing structured data for analysis:
        - transcript: Full transcript text
        - scorecard: Scorecard content
        - candidate_name: Candidate name if provided
        - analysis_ready: Boolean indicating data is ready for LLM analysis
    """
    return {
        "transcript": transcript_content,
        "scorecard": scorecard_content,
        "candidate_name": candidate_name,
        "analysis_ready": True,
        "note": "This tool structures the data. The agent's LLM will analyze the transcript against scorecard criteria."
    }


def analyze_transcript_from_page_id(
    transcript_page_id: str,
    scorecard_content: str,
    candidate_name: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze an interview transcript from a Notion page ID against scorecard criteria.
    
    Convenience function that fetches transcript content and structures it for analysis.
    
    Args:
        transcript_page_id: Notion page ID of the transcript
        scorecard_content: Scorecard criteria text/content from Notion page
        candidate_name: Optional candidate name for context
    
    Returns:
        Dictionary containing structured data for analysis (same format as analyze_transcript)
    """
    # Fetch transcript content
    transcript_data = get_transcript_content(transcript_page_id)
    transcript_content = transcript_data.get("transcript", "")
    
    return analyze_transcript(
        transcript_content=transcript_content,
        scorecard_content=scorecard_content,
        candidate_name=candidate_name
    )
