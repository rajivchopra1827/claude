"""Parse strategic priority mappings from rajiv_context.md."""

import re
from typing import Dict, Any, Optional, List
from .get_rajiv_context import get_rajiv_context


def _extract_section(content: str, section_title: str) -> str:
    """Extract a specific section from markdown content.
    
    Args:
        content: Full markdown content
        section_title: Section title to extract (e.g., "Strategic Priority Mappings")
        
    Returns:
        Section content as string, or empty string if not found
    """
    # Match section header and capture everything until next ## or end of file
    pattern = rf"^##\s+\d+\.\s+{re.escape(section_title)}.*?(?=^##\s+\d+\.|$)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(0)
    # Try without number prefix (in case format differs)
    pattern2 = rf"^##\s+{re.escape(section_title)}.*?(?=^##\s+|$)"
    match2 = re.search(pattern2, content, re.MULTILINE | re.DOTALL)
    return match2.group(0) if match2 else ""


def _parse_priority_section(section_text: str) -> Dict[str, Any]:
    """Parse a single priority section (e.g., "Priority 1: Fiona 2.0").
    
    Args:
        section_text: Text for one priority section
        
    Returns:
        Dict with priority info: name, display_name, keywords, people, etc.
    """
    result = {
        "keywords": [],
        "people": [],
        "exclusions": []  # Terms that should NOT match this priority
    }
    
    # Extract priority name from header (e.g., "Priority 1: Fiona 2.0 (Marketing Intelligence)")
    header_match = re.search(r"###\s+Priority\s+\d+:\s+(.+?)(?:\n|$)", section_text)
    if header_match:
        full_name = header_match.group(1).strip()
        # Split display name from short name
        if "(" in full_name:
            result["name"] = full_name.split("(")[0].strip()
            result["display_name"] = full_name
        else:
            result["name"] = full_name
            result["display_name"] = full_name
    
    # Extract "Also known as:" keywords
    also_known_match = re.search(r"\*\*Also known as:\*\*\s*(.+?)(?:\n|$)", section_text)
    if also_known_match:
        also_known = also_known_match.group(1).strip()
        # Split by comma and clean up
        keywords = [kw.strip().lower() for kw in also_known.split(",")]
        result["keywords"].extend(keywords)
    
    # Extract people from Lead, Key partners, etc.
    lead_match = re.search(r"\*\*Lead:\*\*\s*(.+?)(?:\n|$)", section_text)
    if lead_match:
        lead_text = lead_match.group(1).strip()
        # Extract names (e.g., "Kelsey (Lead PM), Cassidy (Tech Lead)")
        names = re.findall(r"([A-Z][a-z]+)\s*\(", lead_text)
        result["people"].extend([name.lower() for name in names])
    
    key_partners_match = re.search(r"\*\*Key partners:\*\*\s*(.+?)(?:\n|$)", section_text)
    if key_partners_match:
        partners_text = key_partners_match.group(1).strip()
        names = re.findall(r"([A-Z][a-z]+)\s*\(", partners_text)
        result["people"].extend([name.lower() for name in names])
    
    agency_partner_match = re.search(r"\*\*Agency partner:\*\*\s*(.+?)(?:\n|$)", section_text)
    if agency_partner_match:
        partner_text = agency_partner_match.group(1).strip()
        names = re.findall(r"([A-Z][a-z]+)\s*\(", partner_text)
        result["people"].extend([name.lower() for name in names])
    
    # Extract keywords from "Related projects/work:" bullet points
    related_match = re.search(r"\*\*Related projects/work:\*\*\s*\n((?:- .+\n?)+)", section_text)
    if related_match:
        bullets = related_match.group(1)
        # Extract text from each bullet (remove "- " and quotes)
        bullet_items = re.findall(r"-\s+(.+?)(?:\n|$)", bullets)
        for item in bullet_items:
            # Remove quotes and extract keywords
            clean_item = item.replace('"', '').strip()
            # Remove markdown links if present
            clean_item = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_item)
            # Add the full phrase as a keyword
            result["keywords"].append(clean_item.lower())
            # Also add individual words (for better matching)
            words = clean_item.lower().split()
            result["keywords"].extend([w for w in words if len(w) > 2])  # Skip short words
    
    # Extract exclusions from Notes
    note_match = re.search(r"\*\*Note:\*\*\s*(.+?)(?:\n|$)", section_text)
    if note_match:
        note_text = note_match.group(1).strip()
        # Look for exclusion patterns (e.g., "Fiona Posts demo" is NOT Fiona 2.0)
        exclusion_match = re.search(r'"([^"]+)"\s+is\s+NOT', note_text, re.IGNORECASE)
        if exclusion_match:
            result["exclusions"].append(exclusion_match.group(1).lower())
    
    return result


def _parse_success_metrics(content: str) -> Dict[str, Dict[str, str]]:
    """Parse success metrics and deadlines from Section 5.
    
    Args:
        content: Full markdown content
        
    Returns:
        Dict mapping priority names to success_metric and deadline
    """
    metrics = {}
    
    # Extract Section 5
    section_5 = _extract_section(content, "Success Metrics")
    if not section_5:
        return metrics
    
    # Parse each priority's metrics
    priority_patterns = {
        "fiona_2": r"\*\*Fiona 2\.0.*?\*\*:?\s*\n((?:- .+\n?)+)",
        "posts": r"\*\*Posts.*?\*\*:?\s*\n((?:- .+\n?)+)",
        "ai_fulfillment": r"\*\*AI Evolution.*?\*\*:?\s*\n((?:- .+\n?)+)",
        "digible_ai": r"\*\*Digible\.AI.*?\*\*:?\s*\n((?:- .+\n?)+)",
    }
    
    for key, pattern in priority_patterns.items():
        match = re.search(pattern, section_5, re.IGNORECASE | re.DOTALL)
        if match:
            bullets = match.group(1)
            # Extract first bullet as success metric
            first_bullet = re.search(r"-\s+(.+?)(?:\n|$)", bullets)
            if first_bullet:
                metrics[key] = {"success_metric": first_bullet.group(1).strip()}
    
    # Extract deadlines from Section 4 (Strategic Pillars)
    section_4 = _extract_section(content, "Strategic Pillars")
    if section_4:
        # Look for deadline patterns
        deadline_patterns = {
            "fiona_2": r"Fiona 2\.0.*?(\w+\s+\d{4})",
            "digible_ai": r"Digible\.AI.*?(\w+\s+\d{4})",
        }
        for key, pattern in deadline_patterns.items():
            match = re.search(pattern, section_4, re.IGNORECASE)
            if match:
                if key not in metrics:
                    metrics[key] = {}
                metrics[key]["deadline"] = match.group(1)
    
    # Add defaults for missing priorities
    defaults = {
        "posts": {"success_metric": "$100k direct MRR by EOY 2026", "deadline": "End of 2026"},
        "ai_fulfillment": {"success_metric": "Increase efficiency, increase Accounts/FTE", "deadline": "Ongoing"},
        "ai_enablement": {"success_metric": "Org-wide AI adoption", "deadline": "Ongoing"},
    }
    
    for key, default in defaults.items():
        if key not in metrics:
            metrics[key] = default
    
    return metrics


def _parse_people_table(content: str) -> Dict[str, str]:
    """Parse People → Pod → Priority table.
    
    Args:
        content: Full markdown content
        
    Returns:
        Dict mapping person names (lowercase) to priority keys
    """
    people_map = {}
    
    # Find Section 7 directly (it's the last section)
    section_7_start = content.find("## 7. Strategic Priority Mappings")
    if section_7_start == -1:
        return people_map
    section_7 = content[section_7_start:]
    
    # Find the People table
    table_match = re.search(r"###\s+People.*?Priority Quick Reference.*?\n((?:\|.*\|\n?)+)", section_7, re.DOTALL)
    if not table_match:
        return people_map
    
    table_text = table_match.group(1)
    # Parse table rows (skip header row)
    rows = [row.strip() for row in table_text.split("\n") if row.strip() and not row.startswith("|---")]
    
    # Priority name to key mapping (case-insensitive matching)
    priority_name_to_key = {
        "fiona 2.0": "fiona_2",
        "fiona": "fiona_2",
        "posts": "posts",
        "ai fulfillment": "ai_fulfillment",
        "fulfillment": "ai_fulfillment",
        "digible.ai": "digible_ai",
        "digible ai": "digible_ai",
        "ai enablement": "ai_enablement",
        "enablement": "ai_enablement",
    }
    
    for row in rows[1:]:  # Skip header
        # Parse: | Person | Pod | Primary Priority |
        parts = [p.strip() for p in row.split("|") if p.strip()]
        if len(parts) >= 3:
            person = parts[0].lower()
            # Skip entries with brackets like [Open Director]
            if person.startswith("[") and person.endswith("]"):
                continue
            priority_name = parts[2].lower()
            
            # Handle "All" priority (skip it)
            if "all" in priority_name:
                continue
            
            # Map priority name to key
            for name, key in priority_name_to_key.items():
                if name in priority_name:
                    people_map[person] = key
                    break
    
    return people_map


def get_strategic_priorities() -> Dict[str, Dict[str, Any]]:
    """Get strategic priorities parsed from rajiv_context.md.
    
    Returns:
        Dict matching the format of the old STRATEGIC_PRIORITIES constant:
        {
            "fiona_2": {
                "name": "Fiona 2.0",
                "display_name": "Fiona 2.0 (Marketing Intelligence)",
                "keywords": [...],
                "people": [...],
                "success_metric": "...",
                "deadline": "..."
            },
            ...
        }
    """
    context = get_rajiv_context()
    content = context["content"]
    
    # Find Section 7 start position
    section_7_start = content.find("## 7. Strategic Priority Mappings")
    if section_7_start == -1:
        # Fallback to empty structure
        return {}
    
    # Get everything from Section 7 to end of file (it's the last section)
    section_7 = content[section_7_start:]
    
    # Parse each priority section individually
    priorities = {}
    priority_keys = ["fiona_2", "posts", "ai_fulfillment", "digible_ai", "ai_enablement"]
    priority_numbers = [1, 2, 3, 4, 5]
    
    for i, priority_num in enumerate(priority_numbers):
        if i >= len(priority_keys):
            break
        
        # Extract this priority's section
        if i < len(priority_numbers) - 1:
            # Not the last one, match until next priority
            pattern = rf"###\s+Priority\s+{priority_num}:.*?(?=###\s+Priority\s+{priority_numbers[i+1]}:|---|$)"
        else:
            # Last priority, match until end or next major section
            pattern = rf"###\s+Priority\s+{priority_num}:.*?(?=###\s+Cross-Cutting|###\s+People|$)"
        
        match = re.search(pattern, section_7, re.DOTALL)
        if match:
            section_text = match.group(0)
            parsed = _parse_priority_section(section_text)
            if parsed.get("name"):
                priorities[priority_keys[i]] = parsed
    
    # Add success metrics and deadlines from Section 5
    metrics = _parse_success_metrics(content)
    for key in priority_keys:
        if key in priorities and key in metrics:
            priorities[key].update(metrics[key])
    
    # Ensure all priorities have required fields
    for key in priority_keys:
        if key not in priorities:
            priorities[key] = {
                "name": key.replace("_", " ").title(),
                "display_name": key.replace("_", " ").title(),
                "keywords": [],
                "people": [],
                "success_metric": "",
                "deadline": ""
            }
    
    return priorities


def get_priority_by_person(person_name: str) -> Optional[str]:
    """Get strategic priority key for a given person name.
    
    Args:
        person_name: Person's name (e.g., "Kelsey", "Megan")
        
    Returns:
        Priority key (e.g., "fiona_2", "ai_fulfillment") or None if not found
    """
    context = get_rajiv_context()
    content = context["content"]
    
    people_map = _parse_people_table(content)
    return people_map.get(person_name.lower())
