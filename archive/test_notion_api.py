"""Test script for Notion API integration."""

import os
import json
from datetime import date
from dotenv import load_dotenv

# Load environment variables from env.txt
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "env.txt"))

from src.notion_api import (
    get_daily_review,
    get_inbox_tasks,
    get_waiting_tasks,
    get_overdue_tasks,
    extract_task_properties,
    create_task,
    update_task,
    search_projects,
    fetch_page
)

def test_daily_review():
    """Test daily review retrieval."""
    print("=" * 60)
    print("Testing Daily Review")
    print("=" * 60)
    
    review = get_daily_review()
    
    print(f"\nTop Priority: {len(review['top_priority'])} tasks")
    for task in review['top_priority']:
        print(f"  - {task['title']}")
        if task.get('due_date'):
            print(f"    Due: {task['due_date']}")
    
    print(f"\nThis Week: {len(review['this_week'])} tasks")
    for task in review['this_week'][:5]:  # Show first 5
        print(f"  - {task['title']}")
        if task.get('due_date'):
            print(f"    Due: {task['due_date']}")
    if len(review['this_week']) > 5:
        print(f"  ... and {len(review['this_week']) - 5} more")
    
    print(f"\nOn Deck: {len(review['on_deck'])} tasks")
    for task in review['on_deck']:
        print(f"  - {task['title']}")
    
    print(f"\nWaiting: {len(review['waiting'])} tasks")
    for task in review['waiting']:
        print(f"  - {task['title']}")
        if task.get('waiting'):
            print(f"    Waiting on: {', '.join(task['waiting'])}")
    
    print(f"\nOverdue: {len(review['overdue'])} tasks")
    for task in review['overdue']:
        print(f"  - {task['title']}")
        if task.get('due_date'):
            print(f"    Due: {task['due_date']}")
    
    print("\n✓ Daily review test passed\n")


def test_inbox_tasks():
    """Test inbox task retrieval."""
    print("=" * 60)
    print("Testing Inbox Tasks")
    print("=" * 60)
    
    inbox_tasks = get_inbox_tasks()
    print(f"\nFound {len(inbox_tasks)} tasks in Inbox")
    
    for task in inbox_tasks[:5]:  # Show first 5
        props = extract_task_properties(task)
        print(f"  - {props['title']}")
        if props.get('project_ids'):
            print(f"    Project IDs: {props['project_ids']}")
    
    if len(inbox_tasks) > 5:
        print(f"  ... and {len(inbox_tasks) - 5} more")
    
    print("\n✓ Inbox tasks test passed\n")


def test_waiting_tasks():
    """Test waiting tasks retrieval."""
    print("=" * 60)
    print("Testing Waiting Tasks")
    print("=" * 60)
    
    waiting_tasks = get_waiting_tasks()
    print(f"\nFound {len(waiting_tasks)} tasks in Waiting")
    
    for task in waiting_tasks:
        props = extract_task_properties(task)
        print(f"  - {props['title']}")
        if props.get('waiting'):
            print(f"    Waiting on: {', '.join(props['waiting'])}")
        if props.get('created_time'):
            print(f"    Created: {props['created_time']}")
    
    print("\n✓ Waiting tasks test passed\n")


def test_overdue_tasks():
    """Test overdue tasks retrieval."""
    print("=" * 60)
    print("Testing Overdue Tasks")
    print("=" * 60)
    
    overdue_tasks = get_overdue_tasks()
    print(f"\nFound {len(overdue_tasks)} overdue tasks")
    
    for task in overdue_tasks:
        props = extract_task_properties(task)
        print(f"  - {props['title']}")
        if props.get('due_date'):
            print(f"    Due: {props['due_date']}")
        print(f"    Status: {props['status']}")
    
    print("\n✓ Overdue tasks test passed\n")


def test_search_projects():
    """Test project search."""
    print("=" * 60)
    print("Testing Project Search")
    print("=" * 60)
    
    # Search for a common project
    projects = search_projects("Reporting")
    print(f"\nFound {len(projects)} projects matching 'Reporting'")
    
    for project in projects[:3]:  # Show first 3
        props = project.get('properties', {})
        name_obj = props.get('Name', {}).get('title', [])
        if name_obj:
            name = name_obj[0].get('plain_text', 'Unknown')
            print(f"  - {name}")
            print(f"    ID: {project.get('id')}")
    
    print("\n✓ Project search test passed\n")


def test_create_task():
    """Test task creation (commented out to avoid creating test tasks)."""
    print("=" * 60)
    print("Testing Task Creation (SKIPPED - uncomment to test)")
    print("=" * 60)
    
    # Uncomment to test:
    # test_task = create_task(
    #     name="Test Task - Please Delete",
    #     status="Inbox",
    #     due_date="2026-01-20"
    # )
    # print(f"\nCreated test task: {test_task.get('id')}")
    # print(f"URL: {test_task.get('url')}")
    # print("\n⚠️  Please delete this test task manually")
    
    print("✓ Task creation test skipped (uncomment to test)\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Notion API Test Suite")
    print("=" * 60 + "\n")
    
    # Check API key
    if not os.getenv("NOTION_API_KEY"):
        print("❌ ERROR: NOTION_API_KEY not found in environment")
        print("   Make sure it's set in env.txt")
        exit(1)
    
    print("✓ API key found\n")
    
    try:
        test_daily_review()
        test_inbox_tasks()
        test_waiting_tasks()
        test_overdue_tasks()
        test_search_projects()
        test_create_task()
        
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
