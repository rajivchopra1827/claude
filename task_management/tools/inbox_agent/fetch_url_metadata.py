"""Fetch metadata from a URL (title, description, etc.)."""

import re
from typing import Dict, Any
import httpx


def fetch_url_metadata(url: str) -> Dict[str, Any]:
    """Fetch metadata from a URL (title, description, etc.).
    
    Args:
        url: URL to fetch metadata from
    
    Returns:
        Dictionary with title, description, and other metadata
    """
    try:
        # Simple implementation - fetch HTML and extract title
        # In production, you might want to use a library like beautifulsoup4
        response = httpx.get(url, timeout=10, follow_redirects=True)
        html = response.text
        
        # Extract title from HTML
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else None
        
        # Extract meta description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else None
        
        return {
            "title": title or url,
            "description": description,
            "url": url
        }
    except Exception as e:
        # Return minimal metadata on error
        return {
            "title": url,
            "description": None,
            "url": url,
            "error": str(e)
        }
