"""Infer resource type from URL."""


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
