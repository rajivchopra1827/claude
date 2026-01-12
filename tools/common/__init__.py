"""Shared utilities for Notion API operations."""

from .notion_client import get_notion_client, query_database_complete
from .constants import (
    TASKS_DB_ID,
    TASKS_DATA_SOURCE_ID,
    PROJECTS_DB_ID,
    PROJECTS_DATA_SOURCE_ID,
    RESOURCES_DB_ID,
    INSIGHTS_DB_ID,
    PM_COMPETENCY_MODEL_ID,
)

__all__ = [
    "get_notion_client",
    "query_database_complete",
    "TASKS_DB_ID",
    "TASKS_DATA_SOURCE_ID",
    "PROJECTS_DB_ID",
    "PROJECTS_DATA_SOURCE_ID",
    "RESOURCES_DB_ID",
    "INSIGHTS_DB_ID",
    "PM_COMPETENCY_MODEL_ID",
]
