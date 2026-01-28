"""Tools for Context Gathering Agent - searching and retrieving context from Notion.

NOTE: These tools have been moved to tools.notion for shared access.
This module re-exports from tools.notion for backward compatibility.
"""

# Re-export from tools.notion for backward compatibility
from tools.notion import (
    search_transcripts,
    get_transcript,
    get_transcript_content,
    extract_action_items,
    extract_action_items_from_transcript,
    extract_action_items_from_notes,
)
# Import from common for backward compatibility
from tools.common import get_rajiv_context as get_work_context

__all__ = [
    "search_transcripts",
    "get_transcript",
    "get_transcript_content",
    "extract_action_items",
    "extract_action_items_from_transcript",
    "extract_action_items_from_notes",
    "get_work_context",  # Backward compatibility alias
]
