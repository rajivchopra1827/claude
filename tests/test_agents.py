"""Simple test script for agents (requires dependencies to be installed first).

Run after: pip install -r requirements.txt
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from agents.router import route_to_agent
        print("✓ Router imports OK")
    except Exception as e:
        print(f"✗ Router import failed: {e}")
        return False
    
    try:
        from agents.inbox_agent import inbox_agent
        print("✓ Inbox agent imports OK")
    except Exception as e:
        print(f"✗ Inbox agent import failed: {e}")
        return False
    
    try:
        from agents.task_manager_agent import task_manager_agent
        print("✓ Task manager agent imports OK")
    except Exception as e:
        print(f"✗ Task manager agent import failed: {e}")
        return False
    
    try:
        from agents.interview_assistant_agent import interview_assistant_agent
        print("✓ Interview assistant agent imports OK")
    except Exception as e:
        print(f"✗ Interview assistant agent import failed: {e}")
        return False
    
    return True


def test_routing():
    """Test router functionality."""
    print("\nTesting routing...")
    
    try:
        from agents.router import route_to_agent
        
        # Test inbox routing
        agent = route_to_agent("Save this article: https://example.com")
        assert agent.name == "Inbox Agent", f"Expected Inbox Agent, got {agent.name}"
        print("✓ Inbox routing works")
        
        # Test task manager routing
        agent = route_to_agent("What should I work on today?")
        assert agent.name == "Task Manager Agent", f"Expected Task Manager Agent, got {agent.name}"
        print("✓ Task manager routing works")
        
        # Test interview routing
        agent = route_to_agent("Analyze this interview transcript")
        assert agent.name == "Interview Assistant Agent", f"Expected Interview Assistant Agent, got {agent.name}"
        print("✓ Interview assistant routing works")
        
        return True
    except Exception as e:
        print(f"✗ Routing test failed: {e}")
        return False


def test_tools():
    """Test that tools can be imported."""
    print("\nTesting tools...")
    
    try:
        from tools.inbox_agent import create_task, create_resource, create_insight
        print("✓ Inbox agent tools import OK")
    except Exception as e:
        print(f"✗ Inbox agent tools import failed: {e}")
        return False
    
    try:
        from tools.task_manager_agent import get_daily_review, update_task
        print("✓ Task manager agent tools import OK")
    except Exception as e:
        print(f"✗ Task manager agent tools import failed: {e}")
        return False
    
    try:
        from tools.interview_assistant_agent import fetch_page
        print("✓ Interview assistant agent tools import OK")
    except Exception as e:
        print(f"✗ Interview assistant agent tools import failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Agent System Test")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_tools()
    all_passed &= test_routing()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set NOTION_API_KEY in env.txt")
        print("3. Test with: python main.py 'What should I work on today?'")
    else:
        print("✗ Some tests failed. Check errors above.")
    print("=" * 50)
