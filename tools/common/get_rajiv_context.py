"""Get Rajiv context - role, team, strategy, and decision-making framework."""

import os
import re
from typing import Dict, Any

def get_rajiv_context() -> Dict[str, Any]:
    """Get Rajiv's complete context document.
    
    Returns:
        Dictionary with:
        - content: Full markdown content of the Rajiv context document
        - last_updated: Last updated date from the document (if found)
    """
    # Get project root (assuming this file is in tools/common/)
    # File structure: project_root/tools/common/get_rajiv_context.py
    # So we need to go up 2 levels from the file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Path to Rajiv context file
    context_file = os.path.join(project_root, "context", "rajiv_context.md")
    
    # Read the file
    with open(context_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract last_updated date if present (look for "*Last updated: ..." pattern)
    last_updated = None
    match = re.search(r'\*Last updated:\s*([^*]+)\*', content)
    if match:
        last_updated = match.group(1).strip()
    
    return {
        "content": content,
        "last_updated": last_updated,
    }
