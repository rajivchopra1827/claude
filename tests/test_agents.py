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
        from agents.orchestrator_team import orchestrator_team
        print("✓ Orchestrator team imports OK")
    except Exception as e:
        print(f"✗ Orchestrator team import failed: {e}")
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
    
    try:
        from agents.context_gathering_agent import context_gathering_agent
        print("✓ Context gathering agent imports OK")
    except Exception as e:
        print(f"✗ Context gathering agent import failed: {e}")
        return False
    
    return True


def test_orchestrator():
    """Test orchestrator team functionality."""
    print("\nTesting orchestrator team...")
    
    try:
        from agents.orchestrator_team import orchestrator_team
        
        # Verify team configuration
        assert orchestrator_team.name == "Work Hub Orchestrator", f"Expected 'Work Hub Orchestrator', got {orchestrator_team.name}"
        assert len(orchestrator_team.members) == 4, f"Expected 4 members, got {len(orchestrator_team.members)}"
        assert orchestrator_team.respond_directly == True, "Expected respond_directly=True"
        assert orchestrator_team.determine_input_for_members == False, "Expected determine_input_for_members=False"
        print("✓ Orchestrator team configuration correct")
        
        # Verify all agents are members
        member_names = [m.name for m in orchestrator_team.members]
        expected_agents = ["Inbox Agent", "Task Manager Agent", "Context Gathering Agent", "Interview Assistant Agent"]
        for agent_name in expected_agents:
            assert agent_name in member_names, f"Expected {agent_name} to be a team member"
        print("✓ All agents are team members")
        
        return True
    except Exception as e:
        print(f"✗ Orchestrator test failed: {e}")
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
    all_passed &= test_orchestrator()
    
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
