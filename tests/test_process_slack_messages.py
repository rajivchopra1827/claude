"""Tests for process_slack_messages.py refactored functions."""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock, patch, call

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from task_management.tools.slack_inbox_agent.process_slack_messages import (
    _get_user_name,
    _build_enhanced_text,
    _log_error_to_debug_file,
    _process_thread_reply,
    _create_notion_entry_from_classification,
    _handle_resource_creation_retry,
    _mark_message_read_if_requested,
)


class TestGetUserName(unittest.TestCase):
    """Test _get_user_name() helper function."""
    
    def test_get_user_name_success(self):
        """Test successful user name retrieval."""
        client = Mock()
        client.users_info.return_value = {
            "ok": True,
            "user": {"real_name": "John Doe", "name": "johndoe"}
        }
        
        result = _get_user_name(client, "user123")
        self.assertEqual(result, "John Doe")
        client.users_info.assert_called_once_with(user="user123")
    
    def test_get_user_name_fallback_to_name(self):
        """Test fallback to 'name' when 'real_name' not available."""
        client = Mock()
        client.users_info.return_value = {
            "ok": True,
            "user": {"name": "johndoe"}
        }
        
        result = _get_user_name(client, "user123")
        self.assertEqual(result, "johndoe")
    
    def test_get_user_name_no_user_id(self):
        """Test with None user_id."""
        client = Mock()
        result = _get_user_name(client, None)
        self.assertIsNone(result)
        client.users_info.assert_not_called()
    
    def test_get_user_name_api_error(self):
        """Test handling of API error."""
        client = Mock()
        client.users_info.side_effect = Exception("API Error")
        
        result = _get_user_name(client, "user123")
        self.assertIsNone(result)
    
    def test_get_user_name_not_ok(self):
        """Test handling when API returns ok=False."""
        client = Mock()
        client.users_info.return_value = {"ok": False}
        
        result = _get_user_name(client, "user123")
        self.assertIsNone(result)


class TestBuildEnhancedText(unittest.TestCase):
    """Test _build_enhanced_text() helper function."""
    
    def test_with_rich_content(self):
        """Test building text with rich content summary."""
        message_text = "Hello world"
        rich_content_summary = "Found 2 links"
        
        result = _build_enhanced_text(message_text, rich_content_summary)
        self.assertEqual(result, "Hello world\n\nFound 2 links")
    
    def test_without_rich_content(self):
        """Test building text without rich content summary."""
        message_text = "Hello world"
        
        result = _build_enhanced_text(message_text, None)
        self.assertEqual(result, "Hello world")
    
    def test_empty_message(self):
        """Test with empty message."""
        result = _build_enhanced_text("", "summary")
        self.assertEqual(result, "\n\nsummary")


class TestLogErrorToDebugFile(unittest.TestCase):
    """Test _log_error_to_debug_file() helper function."""
    
    @patch('builtins.open', create=True)
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.time')
    @patch('json.dumps')
    def test_log_error_success(self, mock_json_dumps, mock_time, mock_open):
        """Test successful error logging."""
        mock_time.time.return_value = 1234567.89
        mock_json_dumps.return_value = '{"test": "data"}'
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        _log_error_to_debug_file("Test error", "test.py:123", {"key": "value"})
        
        mock_open.assert_called_once()
        mock_json_dumps.assert_called_once()
        mock_file.write.assert_called_once()
    
    @patch('builtins.open', create=True)
    def test_log_error_file_error(self, mock_open):
        """Test handling of file write error."""
        mock_open.side_effect = Exception("File error")
        
        # Should not raise exception
        _log_error_to_debug_file("Test error", "test.py:123", {})


class TestProcessThreadReply(unittest.TestCase):
    """Test _process_thread_reply() function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.reply = {
            "ts": "1234567890.123456",
            "text": "This is a reply",
            "user": "user123"
        }
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.get_message_id')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.is_message_processed')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.extract_rich_content')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.format_rich_content_summary')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_idea')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.mark_message_processed')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages._get_user_name')
    def test_process_thread_reply_success(
        self, mock_get_user_name, mock_mark_processed, mock_create_idea,
        mock_format_summary, mock_extract_content, mock_is_processed, mock_get_id
    ):
        """Test successful thread reply processing."""
        mock_get_id.return_value = "msg_id_123"
        mock_is_processed.return_value = False
        mock_get_user_name.return_value = "John Doe"
        mock_extract_content.return_value = {}
        mock_format_summary.return_value = None
        mock_create_idea.return_value = {
            "id": "idea_123",
            "url": "https://notion.so/idea_123"
        }
        
        result = _process_thread_reply(
            reply=self.reply,
            client=self.client,
            channel_id="channel123",
            channel_name="test-channel",
            is_dm=False,
            reprocess=False
        )
        
        self.assertIsNotNone(result)
        self.assertFalse(result["skipped"])
        self.assertEqual(result["created_item"]["type"], "idea")
        self.assertEqual(result["counts"]["ideas"], 1)
        mock_create_idea.assert_called_once()
        mock_mark_processed.assert_called_once()
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.get_message_id')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.is_message_processed')
    def test_process_thread_reply_already_processed(
        self, mock_is_processed, mock_get_id
    ):
        """Test skipping already processed reply."""
        mock_get_id.return_value = "msg_id_123"
        mock_is_processed.return_value = True
        
        result = _process_thread_reply(
            reply=self.reply,
            client=self.client,
            channel_id="channel123",
            channel_name="test-channel",
            is_dm=False,
            reprocess=False
        )
        
        self.assertIsNotNone(result)
        self.assertTrue(result["skipped"])
    
    def test_process_thread_reply_no_timestamp(self):
        """Test handling reply without timestamp."""
        reply_no_ts = {"text": "No timestamp"}
        
        result = _process_thread_reply(
            reply=reply_no_ts,
            client=self.client,
            channel_id="channel123",
            channel_name="test-channel",
            is_dm=False,
            reprocess=False
        )
        
        self.assertIsNone(result)
    
    def test_process_thread_reply_empty_text(self):
        """Test handling reply with empty text."""
        reply_empty = {"ts": "1234567890.123456", "text": ""}
        
        with patch('task_management.tools.slack_inbox_agent.process_slack_messages.get_message_id') as mock_get_id, \
             patch('tools.slack_inbox_agent.process_slack_messages.is_message_processed') as mock_is_processed, \
             patch('tools.slack_inbox_agent.process_slack_messages.mark_message_processed') as mock_mark:
            mock_get_id.return_value = "msg_id_123"
            mock_is_processed.return_value = False
            
            result = _process_thread_reply(
                reply=reply_empty,
                client=self.client,
                channel_id="channel123",
                channel_name="test-channel",
                is_dm=False,
                reprocess=False
            )
            
            self.assertIsNotNone(result)
            self.assertTrue(result["skipped"])
            mock_mark.assert_called_once()


class TestCreateNotionEntryFromClassification(unittest.TestCase):
    """Test _create_notion_entry_from_classification() function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classification_task = {"classification": "TASK", "urls": []}
        self.classification_resource = {"classification": "RESOURCE", "urls": ["https://example.com"]}
        self.classification_idea = {"classification": "IDEA", "urls": []}
        self.classification_multiple = {"classification": "MULTIPLE", "urls": ["https://example.com"]}
        
        self.message_text = "Test message"
        self.rich_content_summary = "Summary"
        self.rich_content = {"links": []}
        self.channel_name = "test-channel"
        self.is_dm = False
        self.user_name = "John Doe"
        self.enhanced_text = "Test message\n\nSummary"
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_task')
    def test_create_task(self, mock_create_task):
        """Test creating a task entry."""
        mock_create_task.return_value = {
            "id": "task_123",
            "url": "https://notion.so/task_123"
        }
        
        result = _create_notion_entry_from_classification(
            classification=self.classification_task,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            is_dm=self.is_dm,
            user_name=self.user_name,
            enhanced_text=self.enhanced_text
        )
        
        self.assertEqual(result["notion_type"], "task")
        self.assertEqual(result["notion_id"], "task_123")
        self.assertEqual(result["counts"]["tasks"], 1)
        self.assertEqual(len(result["created_items"]), 1)
        mock_create_task.assert_called_once()
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.fetch_url_metadata')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.infer_resource_type')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_resource')
    def test_create_resource(
        self, mock_create_resource, mock_infer_type, mock_fetch_metadata
    ):
        """Test creating a resource entry."""
        mock_fetch_metadata.return_value = {"title": "Example Site"}
        mock_infer_type.return_value = "Article"
        mock_create_resource.return_value = {
            "id": "resource_123",
            "url": "https://notion.so/resource_123"
        }
        
        result = _create_notion_entry_from_classification(
            classification=self.classification_resource,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            is_dm=self.is_dm,
            user_name=self.user_name,
            enhanced_text=self.enhanced_text
        )
        
        self.assertEqual(result["notion_type"], "resource")
        self.assertEqual(result["notion_id"], "resource_123")
        self.assertEqual(result["counts"]["resources"], 1)
        mock_create_resource.assert_called_once()
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_idea')
    def test_create_idea(self, mock_create_idea):
        """Test creating an idea entry."""
        mock_create_idea.return_value = {
            "id": "idea_123",
            "url": "https://notion.so/idea_123"
        }
        
        result = _create_notion_entry_from_classification(
            classification=self.classification_idea,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            is_dm=self.is_dm,
            user_name=self.user_name,
            enhanced_text=self.enhanced_text
        )
        
        self.assertEqual(result["notion_type"], "idea")
        self.assertEqual(result["notion_id"], "idea_123")
        self.assertEqual(result["counts"]["ideas"], 1)
        mock_create_idea.assert_called_once()
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.fetch_url_metadata')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.infer_resource_type')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_resource')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_task')
    def test_create_multiple(
        self, mock_create_task, mock_create_resource, mock_infer_type, mock_fetch_metadata
    ):
        """Test creating multiple entries (resource + task)."""
        mock_fetch_metadata.return_value = {"title": "Example Site"}
        mock_infer_type.return_value = "Article"
        mock_create_resource.return_value = {"id": "resource_123"}
        mock_create_task.return_value = {"id": "task_123"}
        
        result = _create_notion_entry_from_classification(
            classification=self.classification_multiple,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            is_dm=self.is_dm,
            user_name=self.user_name,
            enhanced_text=self.enhanced_text
        )
        
        self.assertEqual(result["notion_type"], "resource")
        self.assertEqual(result["counts"]["resources"], 1)
        self.assertEqual(result["counts"]["tasks"], 1)
        self.assertEqual(len(result["created_items"]), 2)
        mock_create_resource.assert_called_once()
        mock_create_task.assert_called_once()


class TestHandleResourceCreationRetry(unittest.TestCase):
    """Test _handle_resource_creation_retry() function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classification = {
            "classification": "RESOURCE",
            "urls": ["https://example.com"]
        }
        self.message_text = "Test message"
        self.rich_content_summary = "Summary"
        self.rich_content = {"links": []}
        self.channel_name = "test-channel"
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.fetch_url_metadata')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.infer_resource_type')
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_resource')
    def test_retry_success(
        self, mock_create_resource, mock_infer_type, mock_fetch_metadata
    ):
        """Test successful retry."""
        mock_fetch_metadata.return_value = {"title": "Example"}
        mock_infer_type.return_value = "Article"
        mock_create_resource.return_value = {"id": "resource_123"}
        
        result = _handle_resource_creation_retry(
            classification=self.classification,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            message_id="msg_123",
            channel_id="channel_123",
            message_ts="1234567890.123456"
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result["notion_id"], "resource_123")
        self.assertEqual(result["notion_type"], "resource")
    
    def test_retry_wrong_classification(self):
        """Test retry with non-RESOURCE classification."""
        classification = {"classification": "TASK"}
        
        result = _handle_resource_creation_retry(
            classification=classification,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            message_id="msg_123",
            channel_id="channel_123",
            message_ts="1234567890.123456"
        )
        
        self.assertIsNone(result)
    
    @patch('task_management.tools.slack_inbox_agent.process_slack_messages.create_resource')
    def test_retry_failure(self, mock_create_resource):
        """Test retry failure."""
        mock_create_resource.side_effect = Exception("Creation failed")
        
        result = _handle_resource_creation_retry(
            classification=self.classification,
            message_text=self.message_text,
            rich_content_summary=self.rich_content_summary,
            rich_content=self.rich_content,
            channel_name=self.channel_name,
            message_id="msg_123",
            channel_id="channel_123",
            message_ts="1234567890.123456"
        )
        
        self.assertIsNone(result)


class TestMarkMessageReadIfRequested(unittest.TestCase):
    """Test _mark_message_read_if_requested() function."""
    
    def test_mark_as_read_true(self):
        """Test marking message as read when requested."""
        client = Mock()
        client.conversations_mark.return_value = {"ok": True}
        
        _mark_message_read_if_requested(
            client=client,
            channel_id="channel123",
            message_ts="1234567890.123456",
            mark_as_read=True
        )
        
        client.conversations_mark.assert_called_once_with(
            channel="channel123",
            ts="1234567890.123456"
        )
    
    def test_mark_as_read_false(self):
        """Test not marking when mark_as_read is False."""
        client = Mock()
        
        _mark_message_read_if_requested(
            client=client,
            channel_id="channel123",
            message_ts="1234567890.123456",
            mark_as_read=False
        )
        
        client.conversations_mark.assert_not_called()
    
    def test_mark_as_read_error(self):
        """Test handling error when marking as read."""
        client = Mock()
        client.conversations_mark.side_effect = Exception("API Error")
        
        # Should not raise exception
        _mark_message_read_if_requested(
            client=client,
            channel_id="channel123",
            message_ts="1234567890.123456",
            mark_as_read=True
        )


if __name__ == "__main__":
    unittest.main()
