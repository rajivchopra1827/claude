"""Load agent instructions and inject Rajiv context."""

import os
import re
from .summarize_rajiv_context import summarize_rajiv_context


def load_agent_instructions(agent_name: str) -> str:
    """Load agent instructions and inject Rajiv context.
    
    Args:
        agent_name: Name of agent (e.g., 'inbox_agent', 'task_manager_agent')
    
    Returns:
        Combined instructions with Rajiv context injected
    """
    # Get the agents directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    instructions_dir = os.path.join(project_root, "agents", "instructions")
    
    # Load agent-specific instructions
    instruction_file = os.path.join(instructions_dir, f"{agent_name}.md")
    
    with open(instruction_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip frontmatter (between --- markers)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            instructions = parts[2].strip()
        else:
            instructions = content.strip()
    else:
        instructions = content.strip()
    
    # Get Rajiv context summary
    context_summary = summarize_rajiv_context()
    
    # Find insertion point: after the personality/role section
    # Look for common patterns that indicate end of personality/role section:
    # - "## Your Mission" or "## Your Role" or "## Core" or "## Notion"
    # - Or after "Response style" if it exists
    
    lines = instructions.split('\n')
    insertion_index = None
    
    # Look for common section markers that come after personality
    section_markers = [
        '## Your Mission',
        '## Your Role',
        '## Core',
        '## Notion',
        '## Capabilities',
        '## Workflow',
    ]
    
    for i, line in enumerate(lines):
        for marker in section_markers:
            if marker in line:
                insertion_index = i
                break
        if insertion_index is not None:
            break
    
    # If no marker found, look for "Response style" and insert after that paragraph
    if insertion_index is None:
        for i, line in enumerate(lines):
            if '**Response style**' in line or 'Response style:' in line:
                # Find the end of this paragraph (next blank line or next ##)
                for j in range(i + 1, len(lines)):
                    if not lines[j].strip() or lines[j].startswith('##'):
                        insertion_index = j
                        break
                break
    
    # Fallback: insert after first ## section if nothing found
    if insertion_index is None:
        for i, line in enumerate(lines):
            if line.startswith('##') and i > 0:
                insertion_index = i
                break
    
    # Final fallback: insert after first 10 lines
    if insertion_index is None:
        insertion_index = 10
    
    # Insert context summary
    lines.insert(insertion_index, '')
    lines.insert(insertion_index + 1, context_summary)
    
    return '\n'.join(lines)
