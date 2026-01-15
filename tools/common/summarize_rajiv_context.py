"""Summarize Rajiv context into a concise quick reference format."""

from .get_rajiv_context import get_rajiv_context


def summarize_rajiv_context() -> str:
    """Extract and format a concise summary of Rajiv context.
    
    Returns:
        Formatted markdown string with key context (~150-200 words)
    """
    return """## Rajiv Context (Quick Reference)

**Role:** SVP of AI and Product at Digible, reports to Reid (CEO)

**Key Accountabilities:**
- Agency Revenue Growth (tech-driven value delivery)
- Agency Efficiency & Capacity (scalability)
- Tech Revenue (Digible.AI + Posts)

**Direct Reports:** Megan (Agency Enablement), Melissa (Designer), Kelsey (Reporting), [Open] Director of Product

**Key Strategic Priorities (Rajiv owns):**
- Expand AI Offerings (Digible.AI by Oct 2026)
- Reinvigorate Tech Pillar (Fiona 2.0 by Oct 2026)

**Decision Framework:** All decisions evaluated on: Gross Revenue, Margin, EBITDA, Culture, Reputation, Connection to north star mission

**Key Constraints:** Organizational silos, difficulty saying no, EPD under capacity

**For detailed context** (team structure, success metrics, strategic details, decision trade-offs), use `get_rajiv_context()` tool."""
