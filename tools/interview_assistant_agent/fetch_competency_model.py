"""Fetch the PM competency model page."""

from typing import Dict, Any
from tools.common import PM_COMPETENCY_MODEL_ID
from .fetch_page import fetch_page


def fetch_competency_model() -> Dict[str, Any]:
    """Fetch the PM competency model page.
    
    Returns:
        PM competency model page object
    """
    return fetch_page(PM_COMPETENCY_MODEL_ID)
