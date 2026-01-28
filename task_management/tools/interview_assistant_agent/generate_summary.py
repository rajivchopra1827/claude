"""Generate structured summary file from interview analysis."""

import os
from typing import Dict, Any, Optional
from datetime import datetime


def generate_summary(
    candidate_name: str,
    analysis_results: Dict[str, Any],
    interview_date: Optional[str] = None,
    interview_number: Optional[int] = None,
    output_dir: str = "scratch/interview-summaries"
) -> Dict[str, Any]:
    """Generate a structured markdown summary file from interview analysis.
    
    Args:
        candidate_name: Name of the candidate
        analysis_results: Dictionary containing analysis results with scorecard evaluations
        interview_date: Date of the interview (YYYY-MM-DD format, optional)
        interview_number: Interview number if multiple interviews (optional)
        output_dir: Directory to save the summary file (default: scratch/interview-summaries)
    
    Returns:
        Dictionary containing:
        - file_path: Path to the generated summary file
        - candidate_name: Candidate name
        - success: Boolean indicating if file was created successfully
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    safe_candidate_name = candidate_name.replace(" ", "_").replace("/", "-")
    date_str = interview_date or datetime.now().strftime("%Y-%m-%d")
    
    if interview_number:
        filename = f"{safe_candidate_name}_{date_str}_interview{interview_number}_summary.md"
    else:
        filename = f"{safe_candidate_name}_{date_str}_summary.md"
    
    file_path = os.path.join(output_dir, filename)
    
    # Generate markdown content
    markdown_content = _format_summary_markdown(
        candidate_name=candidate_name,
        analysis_results=analysis_results,
        interview_date=interview_date
    )
    
    # Write file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return {
            "file_path": file_path,
            "candidate_name": candidate_name,
            "success": True,
            "filename": filename
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "candidate_name": candidate_name,
            "success": False,
            "error": str(e)
        }


def _format_summary_markdown(
    candidate_name: str,
    analysis_results: Dict[str, Any],
    interview_date: Optional[str] = None
) -> str:
    """Format analysis results as markdown summary.
    
    Args:
        candidate_name: Name of the candidate
        analysis_results: Dictionary containing analysis results
        interview_date: Date of the interview (optional)
    
    Returns:
        Formatted markdown string
    """
    lines = []
    
    # Header
    lines.append(f"# Interview Summary: {candidate_name}")
    lines.append("")
    
    if interview_date:
        lines.append(f"**Interview Date:** {interview_date}")
        lines.append("")
    
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Define competency groupings
    builder_operator_competencies = [
        "⚙️ Execution / Org Process",
        "🌱 Org Building / People Management",
        "🤝 Influence"
    ]
    product_leadership_competencies = [
        "🧭 Direction",
        "💡 Insight"
    ]
    
    # If analysis_results contains a formatted summary, use it
    if "summary" in analysis_results:
        lines.append(analysis_results["summary"])
        lines.append("")
    
    # If analysis_results contains scorecard evaluations
    if "scorecard_evaluations" in analysis_results:
        evaluations = analysis_results["scorecard_evaluations"]
        
        # Builder/Operator Competencies Section
        lines.append("## Builder/Operator Competencies")
        lines.append("")
        lines.append("*Critical for Year 1 success - building the machine*")
        lines.append("")
        
        for criterion in builder_operator_competencies:
            if criterion in evaluations:
                _format_competency(lines, criterion, evaluations[criterion])
            else:
                # Try to find a matching key (flexible matching)
                for key in evaluations:
                    if any(term in key.lower() for term in criterion.lower().split("/")):
                        _format_competency(lines, criterion, evaluations[key])
                        break
        
        # Product Leadership Competencies Section
        lines.append("## Product Leadership Competencies")
        lines.append("")
        lines.append("*PM fundamentals that matter ongoing*")
        lines.append("")
        
        for criterion in product_leadership_competencies:
            if criterion in evaluations:
                _format_competency(lines, criterion, evaluations[criterion])
            else:
                # Try to find a matching key (flexible matching)
                for key in evaluations:
                    if any(term in key.lower() for term in criterion.lower().split()):
                        _format_competency(lines, criterion, evaluations[key])
                        break
        
        # Handle any additional competencies not in the standard framework
        handled_keys = set(builder_operator_competencies + product_leadership_competencies)
        for criterion, evaluation in evaluations.items():
            if criterion not in handled_keys and not any(
                term in criterion.lower() 
                for c in handled_keys 
                for term in c.lower().replace("⚙️ ", "").replace("🌱 ", "").replace("🤝 ", "").replace("🧭 ", "").replace("💡 ", "").split("/")
            ):
                lines.append("## Additional Competencies")
                lines.append("")
                _format_competency(lines, criterion, evaluation)
    
    # Overall assessment
    if "overall_assessment" in analysis_results:
        lines.append("## Overall Assessment")
        lines.append("")
        lines.append(analysis_results["overall_assessment"])
        lines.append("")
    
    # Key takeaways
    if "key_takeaways" in analysis_results:
        lines.append("## Key Takeaways")
        lines.append("")
        for takeaway in analysis_results["key_takeaways"]:
            lines.append(f"- {takeaway}")
        lines.append("")
    
    # Follow-up questions
    if "follow_up_questions" in analysis_results:
        lines.append("## Suggested Follow-up Questions")
        lines.append("")
        for question in analysis_results["follow_up_questions"]:
            lines.append(f"- {question}")
        lines.append("")
    
    return "\n".join(lines)


def _format_competency(lines: list, criterion: str, evaluation: Any) -> None:
    """Format a single competency evaluation.
    
    Args:
        lines: List to append formatted lines to
        criterion: Competency name
        evaluation: Evaluation data (dict or string)
    """
    lines.append(f"### {criterion}")
    lines.append("")
    
    if isinstance(evaluation, dict):
        # Show grade prominently if present
        if "grade" in evaluation:
            lines.append(f"**Grade:** {evaluation['grade']}")
            lines.append("")
        
        if "assessment" in evaluation:
            lines.append(f"**Assessment:** {evaluation['assessment']}")
            lines.append("")
        
        if "evidence" in evaluation:
            lines.append("**Evidence:**")
            lines.append("")
            for evidence_item in evaluation["evidence"]:
                if isinstance(evidence_item, dict):
                    if "quote" in evidence_item:
                        lines.append(f"> {evidence_item['quote']}")
                        lines.append("")
                    if "example" in evidence_item:
                        lines.append(f"- {evidence_item['example']}")
                else:
                    lines.append(f"- {evidence_item}")
            lines.append("")
        
        if "strengths" in evaluation:
            lines.append("**Strengths:**")
            lines.append("")
            for strength in evaluation["strengths"]:
                lines.append(f"- {strength}")
            lines.append("")
        
        if "gaps" in evaluation:
            lines.append("**Gaps/Areas for Improvement:**")
            lines.append("")
            for gap in evaluation["gaps"]:
                lines.append(f"- {gap}")
            lines.append("")
    else:
        lines.append(str(evaluation))
        lines.append("")
    
    lines.append("---")
    lines.append("")
