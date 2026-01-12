"""URL tools for Inbox Agent - fetching metadata and inferring types."""

import re
from typing import Optional, Dict, Any
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


def infer_resource_type(url: str) -> str:
    """Infer resource type from URL.
    
    Args:
        url: URL to analyze
    
    Returns:
        Resource type: Article, Video, Podcast, Paper/Report, Tool/Product, Book, Other
    """
    url_lower = url.lower()
    
    # Video platforms
    if any(domain in url_lower for domain in ["youtube.com", "youtu.be", "vimeo.com"]):
        return "Video"
    
    # Podcast platforms
    if any(domain in url_lower for domain in ["spotify.com", "podcasts.apple.com", "anchor.fm", "podcast"]):
        return "Podcast"
    
    # Academic/paper platforms
    if any(domain in url_lower for domain in ["arxiv.org", "researchgate.net", "academia.edu", "scholar.google.com", ".pdf"]):
        return "Paper/Report"
    
    # Tool/product platforms
    if any(domain in url_lower for domain in ["github.com", "producthunt.com", "tool", "app"]):
        return "Tool/Product"
    
    # Book platforms
    if any(domain in url_lower for domain in ["amazon.com", "goodreads.com", "book"]):
        return "Book"
    
    # Default to Article
    return "Article"
