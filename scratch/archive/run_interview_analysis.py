#!/usr/bin/env python3
"""Use the interview assistant agent to analyze transcripts."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_management.agents.interview_assistant_agent import interview_assistant_agent

# Use the agent to analyze transcripts
prompt = """Analyze interview transcripts for the following Director of Product candidates:

1. Aida
2. Adrienne  
3. Kelsey Rose
4. Geoffrey (has 2 interviews)
5. Salim (has 2 interviews)

For each candidate:
- Find their transcripts using find_candidate_transcripts()
- Fetch the scorecard criteria using fetch_scorecard()
- For each transcript, get the full content and analyze it against the scorecard criteria
- Generate structured summary files using generate_summary() saved to scratch/interview-summaries/

Focus on scorecard evaluation - extract evidence, quotes, assess strengths and gaps for each criterion.
"""

print("Running interview analysis through Interview Assistant Agent...")
print("="*60)

response = interview_assistant_agent.run(prompt)
print(response.content)
