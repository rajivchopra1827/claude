"""Tests for main.py streaming helper functions."""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import _extract_tool_name, _extract_agent_name


class TestExtractToolName(unittest.TestCase):
    """Test _extract_tool_name() helper function."""
    
    def test_tool_name_attribute(self):
        """Test extraction when chunk has tool_name attribute."""
        chunk = Mock()
        chunk.tool_name = "test_tool"
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "test_tool")
    
    def test_tool_dict_with_tool_name(self):
        """Test extraction when tool is a dict with tool_name key."""
        chunk = Mock()
        chunk.tool = {"tool_name": "test_tool"}
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "test_tool")
    
    def test_tool_dict_with_name(self):
        """Test extraction when tool is a dict with name key."""
        chunk = Mock()
        chunk.tool = {"name": "test_tool"}
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "test_tool")
    
    def test_tool_object_with_tool_name(self):
        """Test extraction when tool object has tool_name attribute."""
        tool_obj = Mock()
        tool_obj.tool_name = "test_tool"
        chunk = Mock()
        chunk.tool = tool_obj
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "test_tool")
    
    def test_tool_object_with_name(self):
        """Test extraction when tool object has name attribute."""
        tool_obj = Mock()
        tool_obj.name = "test_tool"
        chunk = Mock()
        chunk.tool = tool_obj
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "test_tool")
    
    def test_tool_object_with___name__(self):
        """Test extraction when tool object has __name__ attribute."""
        tool_obj = Mock()
        tool_obj.__name__ = "test_tool"
        chunk = Mock()
        chunk.tool = tool_obj
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "test_tool")
    
    def test_no_tool_name_found(self):
        """Test extraction when no tool name can be found."""
        chunk = Mock()
        del chunk.tool_name
        chunk.tool = None
        result = _extract_tool_name(chunk)
        self.assertIsNone(result)
    
    def test_precedence_tool_name_over_tool(self):
        """Test that tool_name attribute takes precedence over tool attribute."""
        chunk = Mock()
        chunk.tool_name = "direct_tool_name"
        chunk.tool = {"name": "tool_dict_name"}
        result = _extract_tool_name(chunk)
        self.assertEqual(result, "direct_tool_name")


class TestExtractAgentName(unittest.TestCase):
    """Test _extract_agent_name() helper function."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock team members
        self.member1 = Mock()
        self.member1.id = "agent_1"
        self.member1.name = "Agent One"
        
        self.member2 = Mock()
        self.member2.id = "agent_2"
        self.member2.name = "Agent Two"
        
        self.team_members = [self.member1, self.member2]
    
    def test_agent_id_attribute(self):
        """Test extraction when chunk has agent_id attribute."""
        chunk = Mock()
        chunk.agent_id = "agent_1"
        result = _extract_agent_name(chunk, self.team_members)
        self.assertEqual(result, "Agent One")
    
    def test_agent_attribute_as_id(self):
        """Test extraction when chunk has agent attribute as ID."""
        chunk = Mock()
        chunk.agent = "agent_2"
        result = _extract_agent_name(chunk, self.team_members)
        self.assertEqual(result, "Agent Two")
    
    def test_run_agent_with_name(self):
        """Test extraction when chunk.run.agent has name attribute."""
        agent_obj = Mock()
        agent_obj.name = "Direct Agent Name"
        chunk = Mock()
        chunk.run = Mock()
        chunk.run.agent = agent_obj
        result = _extract_agent_name(chunk, self.team_members)
        self.assertEqual(result, "Direct Agent Name")
    
    def test_run_agent_with_id(self):
        """Test extraction when chunk.run.agent has id attribute."""
        agent_obj = Mock()
        agent_obj.id = "agent_1"
        chunk = Mock()
        chunk.run = Mock()
        chunk.run.agent = agent_obj
        result = _extract_agent_name(chunk, self.team_members)
        self.assertEqual(result, "Agent One")
    
    def test_agent_id_not_in_team_members(self):
        """Test extraction when agent_id doesn't match any team member."""
        chunk = Mock()
        chunk.agent_id = "unknown_agent"
        result = _extract_agent_name(chunk, self.team_members)
        self.assertEqual(result, "unknown_agent")
    
    def test_no_agent_info_default(self):
        """Test extraction when no agent info is available."""
        chunk = Mock()
        del chunk.agent_id
        del chunk.agent
        result = _extract_agent_name(chunk, self.team_members)
        self.assertEqual(result, "Agent")
    
    def test_member_name_matches_agent_id(self):
        """Test extraction when member.name matches agent_id."""
        member = Mock()
        member.name = "agent_1"  # name matches the ID we're looking for
        member.id = "different_id"
        chunk = Mock()
        chunk.agent_id = "agent_1"
        result = _extract_agent_name(chunk, [member])
        self.assertEqual(result, "agent_1")
    
    def test_member_string_representation_matches(self):
        """Test extraction when member string representation matches agent_id."""
        member = Mock()
        member.__str__ = Mock(return_value="agent_1")
        member.name = "Agent One"
        chunk = Mock()
        chunk.agent_id = "agent_1"
        result = _extract_agent_name(chunk, [member])
        self.assertEqual(result, "Agent One")


if __name__ == "__main__":
    unittest.main()
