#!/usr/bin/env python3
"""Script to analyze interview transcripts using LLM and generate detailed summaries."""

import os
import sys
import json
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agno.models.openai import OpenAIChat
from task_management.tools.interview_assistant_agent import (
    find_candidate_transcripts,
    generate_summary,
)
from tools.notion import get_transcript_content
from tools.common import get_page_content, SCORECARD_PAGE_ID, query_database_complete


def get_scorecard_content() -> str:
    """Get scorecard content from the database."""
    try:
        pages = query_database_complete(
            database_id=SCORECARD_PAGE_ID,
            use_data_source=False
        )
        
        if pages:
            content_parts = []
            for page in pages[:3]:
                try:
                    page_id = page.get("id")
                    if page_id:
                        content = get_page_content(page_id)
                        content_parts.append(content)
                except Exception:
                    pass
            
            return "\n\n---\n\n".join(content_parts) if content_parts else ""
        
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


def analyze_transcript_with_llm(transcript_content: str, scorecard_content: str, candidate_name: str) -> Dict[str, Any]:
    """Use LLM to analyze transcript against scorecard criteria."""
    
    model = OpenAIChat(id="gpt-4o")
    
    # Truncate transcript if too long (keep first and last portions)
    max_length = 50000  # Leave room for prompt and response
    if len(transcript_content) > max_length:
        transcript_preview = transcript_content[:max_length//2] + "\n\n[... transcript truncated ...]\n\n" + transcript_content[-max_length//2:]
    else:
        transcript_preview = transcript_content
    
    prompt = f"""You are analyzing an interview transcript for a Director of Product candidate named {candidate_name}.

SCORECARD CRITERIA:
{scorecard_content}

TRANSCRIPT:
{transcript_preview}

Analyze this interview transcript against the scorecard criteria above. For each criterion in the scorecard:

1. Extract evidence from the transcript (direct quotes and examples)
2. Assess the candidate's performance/strength on that criterion
3. Identify specific strengths demonstrated
4. Note any gaps or areas not addressed

Provide your analysis in the following JSON format:
{{
    "scorecard_evaluations": {{
        "Criterion Name": {{
            "assessment": "Strong/Moderate/Weak assessment with brief explanation",
            "evidence": [
                {{"quote": "Direct quote from transcript", "context": "Brief context"}},
                {{"example": "Description of example/story told"}}
            ],
            "strengths": ["Strength 1", "Strength 2"],
            "gaps": ["Gap 1", "Gap 2"]
        }}
    }},
    "overall_assessment": "Overall summary paragraph of candidate performance",
    "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"]
}}

Be thorough and evidence-based. Only include criteria that you can evaluate from the transcript. If a criterion isn't addressed, note it in the gaps.
"""
    
    try:
        response = model.complete(prompt)
        content = response.content
        
        # Try to extract JSON from the response
        # Look for JSON block in markdown code fence or plain JSON
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                # If no JSON found, create a structured response from the text
                return {
                    "scorecard_evaluations": {},
                    "overall_assessment": content,
                    "key_takeaways": [],
                    "raw_response": content
                }
        
        analysis = json.loads(json_str)
        return analysis
        
    except Exception as e:
        print(f"    Error in LLM analysis: {e}")
        return {
            "scorecard_evaluations": {},
            "overall_assessment": f"Analysis error: {str(e)}",
            "key_takeaways": [],
            "error": str(e)
        }


def analyze_candidate(candidate_name: str) -> List[Dict[str, Any]]:
    """Analyze all transcripts for a candidate."""
    print(f"\n{'='*60}")
    print(f"Analyzing transcripts for: {candidate_name}")
    print(f"{'='*60}\n")
    
    transcripts = find_candidate_transcripts(candidate_name)
    
    if not transcripts:
        print(f"  No transcripts found for {candidate_name}")
        return []
    
    print(f"  Found {len(transcripts)} transcript(s)")
    
    # Get scorecard content
    scorecard_content = get_scorecard_content()
    print(f"  Scorecard content length: {len(scorecard_content)} characters")
    
    results = []
    for i, transcript in enumerate(transcripts):
        transcript_date = transcript.get("date", "")
        page_id = transcript.get("page_id")
        transcript_name = transcript.get("name", "Unknown")
        
        print(f"\n  Processing transcript {i+1}: {transcript_name} ({transcript_date})")
        
        try:
            # Get transcript content
            transcript_data = get_transcript_content(page_id)
            transcript_content = transcript_data.get("transcript", "")
            
            if not transcript_content:
                print(f"    Warning: No transcript content found")
                continue
            
            print(f"    Transcript length: {len(transcript_content)} characters")
            print(f"    Analyzing with LLM...")
            
            # Analyze with LLM
            analysis_results = analyze_transcript_with_llm(
                transcript_content=transcript_content,
                scorecard_content=scorecard_content,
                candidate_name=candidate_name
            )
            
            print(f"    ✓ Analysis complete")
            
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
            import traceback
            traceback.print_exc()
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
    print("Interview Transcript Analysis (with LLM)")
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
