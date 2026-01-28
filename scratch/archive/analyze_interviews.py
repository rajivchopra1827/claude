#!/usr/bin/env python3
"""Script to analyze interview transcripts and generate summaries."""

import os
import sys
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_management.tools.interview_assistant_agent import (
    find_candidate_transcripts,
    analyze_transcript_from_page_id,
    generate_summary,
)
from tools.notion import get_transcript_content
from tools.common import get_page_content, SCORECARD_PAGE_ID, query_database_complete


def get_scorecard_content() -> str:
    """Get scorecard content from the database."""
    try:
        # Try to get pages from the scorecard database
        pages = query_database_complete(
            database_id=SCORECARD_PAGE_ID,
            use_data_source=False
        )
        
        if pages:
            # Get content from the first page (or combine all)
            content_parts = []
            for page in pages[:3]:  # Limit to first 3 pages
                try:
                    page_id = page.get("id")
                    if page_id:
                        content = get_page_content(page_id)
                        content_parts.append(content)
                except Exception:
                    pass
            
            return "\n\n---\n\n".join(content_parts) if content_parts else ""
        
        # If no pages found, return a basic scorecard structure
        return """# Interview Scorecard

## Evaluation Criteria
- Product Strategy & Vision
- Execution & Delivery
- Leadership & Influence
- Technical Understanding
- Communication
- Cultural Fit
"""
    except Exception as e:
        print(f"Warning: Could not fetch scorecard: {e}")
        return """# Interview Scorecard

## Evaluation Criteria
- Product Strategy & Vision
- Execution & Delivery  
- Leadership & Influence
- Technical Understanding
- Communication
- Cultural Fit
"""


def analyze_candidate(candidate_name: str) -> List[Dict[str, Any]]:
    """Analyze all transcripts for a candidate."""
    print(f"\n{'='*60}")
    print(f"Analyzing transcripts for: {candidate_name}")
    print(f"{'='*60}\n")
    
    # Find transcripts
    transcripts = find_candidate_transcripts(candidate_name)
    
    if not transcripts:
        print(f"  No transcripts found for {candidate_name}")
        return []
    
    print(f"  Found {len(transcripts)} transcript(s)")
    
    # Get scorecard content
    scorecard_content = get_scorecard_content()
    
    results = []
    for i, transcript in enumerate(transcripts):
        transcript_date = transcript.get("date", "")
        page_id = transcript.get("page_id")
        
        print(f"\n  Processing transcript {i+1}: {transcript.get('name', 'Unknown')} ({transcript_date})")
        
        try:
            # Get transcript content
            transcript_data = get_transcript_content(page_id)
            transcript_content = transcript_data.get("transcript", "")
            
            if not transcript_content:
                print(f"    Warning: No transcript content found")
                continue
            
            print(f"    Transcript length: {len(transcript_content)} characters")
            
            # Structure data for analysis (the actual LLM analysis will be done separately)
            # For now, we'll create a basic structure that can be enhanced
            analysis_results = {
                "transcript_preview": transcript_content[:2000] + "..." if len(transcript_content) > 2000 else transcript_content,
                "scorecard_criteria": scorecard_content[:1000] if scorecard_content else "Scorecard criteria not available",
                "note": "Full analysis should be performed using the interview_assistant_agent with LLM capabilities"
            }
            
            # Generate summary file
            interview_num = i + 1 if len(transcripts) > 1 else None
            summary_result = generate_summary(
                candidate_name=candidate_name,
                analysis_results=analysis_results,
                interview_date=transcript_date,
                interview_number=interview_num
            )
            
            if summary_result.get("success"):
                print(f"    ✓ Summary saved: {summary_result.get('filename')}")
                results.append({
                    "candidate": candidate_name,
                    "transcript": transcript,
                    "summary_file": summary_result.get("file_path"),
                    "success": True
                })
            else:
                print(f"    ✗ Failed to generate summary: {summary_result.get('error')}")
                results.append({
                    "candidate": candidate_name,
                    "transcript": transcript,
                    "success": False,
                    "error": summary_result.get("error")
                })
                
        except Exception as e:
            print(f"    ✗ Error processing transcript: {e}")
            results.append({
                "candidate": candidate_name,
                "transcript": transcript,
                "success": False,
                "error": str(e)
            })
    
    return results


def main():
    """Main function to analyze all candidates."""
    candidates = ["Aida", "Adrienne", "Kelsey Rose", "Geoffrey", "Salim"]
    
    print("="*60)
    print("Interview Transcript Analysis")
    print("="*60)
    print(f"\nCandidates to analyze: {', '.join(candidates)}")
    print(f"Output directory: scratch/interview-summaries/\n")
    
    all_results = []
    for candidate in candidates:
        results = analyze_candidate(candidate)
        all_results.extend(results)
    
    # Summary
    print(f"\n{'='*60}")
    print("Analysis Complete")
    print(f"{'='*60}\n")
    
    successful = sum(1 for r in all_results if r.get("success"))
    total = len(all_results)
    
    print(f"Processed: {successful}/{total} transcripts successfully")
    print(f"\nSummary files saved to: scratch/interview-summaries/")
    
    if successful < total:
        print(f"\nFailed transcripts:")
        for result in all_results:
            if not result.get("success"):
                print(f"  - {result['candidate']}: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
