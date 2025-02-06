import os
import pytest
from unittest.mock import patch, MagicMock
from ruv_cli.commands.agent.comms_agent import (
    CommsAgent,
    handle_communication,
    SLACK_AVAILABLE
)

@pytest.fixture
def mock_slack():
    """Mock Slack client"""
    if not SLACK_AVAILABLE:
        pytest.skip("Slack SDK not installed")
        
    with patch('ruv_cli.commands.agent.comms_agent.WebClient') as mock:
        client = MagicMock()
        mock.return_value = client
        
        # Mock successful message
        response = {'ts': '1234567890.123456'}
        client.chat_postMessage.return_value = response
        
        yield mock

@pytest.fixture
def mock_smtp():
    """Mock SMTP client"""
    with patch('ruv_cli.commands.agent.comms_agent.smtplib.SMTP') as mock:
        smtp = MagicMock()
        mock.return_value.__enter__.return_value = smtp
        yield mock

@pytest.fixture
def setup_env():
    """Set up environment variables"""
    os.environ.update({
        'SLACK_BOT_TOKEN': 'test_token',
        'EMAIL_SMTP_SERVER': 'smtp.test.com',
        'EMAIL_SMTP_USER': 'test@test.com',
        'EMAIL_SMTP_PASS': 'test_pass',
        'EMAIL_RECIPIENT': 'recipient@test.com'
    })
    yield
    for key in ['SLACK_BOT_TOKEN', 'EMAIL_SMTP_SERVER', 'EMAIL_SMTP_USER', 
                'EMAIL_SMTP_PASS', 'EMAIL_RECIPIENT']:
        if key in os.environ:
            del os.environ[key]

def test_comms_agent_initialization():
    """Should initialize with default name"""
    agent = CommsAgent()
    assert agent.name == "CommsAgent"
    
    agent = CommsAgent(name="CustomAgent")
    assert agent.name == "CustomAgent"

def test_comms_agent_no_method():
    """Should fail when no method provided"""
    agent = CommsAgent()
    result = agent.run("")
    assert result == ""

def test_comms_agent_invalid_method():
    """Should fail with invalid method"""
    agent = CommsAgent()
    result = agent.run("invalid")
    assert result == ""

@pytest.mark.skipif(not SLACK_AVAILABLE, reason="Slack SDK not installed")
def test_slack_message_success(setup_env, mock_slack):
    """Should send Slack message successfully"""
    agent = CommsAgent()
    result = agent.run("slack", "Test message")
    assert "Message sent to Slack" in result
    
    # Verify Slack client called correctly
    mock_slack.assert_called_once_with(token='test_token')
    mock_slack.return_value.chat_postMessage.assert_called_once_with(
        channel='#general',
        text='Test message'
    )

@pytest.mark.skipif(not SLACK_AVAILABLE, reason="Slack SDK not installed")
def test_slack_message_no_token(mock_slack):
    """Should fail when Slack token not set"""
    agent = CommsAgent()
    result = agent.run("slack", "Test message")
    assert result == ""
    
    # Verify Slack client not called
    mock_slack.assert_not_called()

@pytest.mark.skipif(not SLACK_AVAILABLE, reason="Slack SDK not installed")
def test_slack_message_api_error(setup_env, mock_slack):
    """Should handle Slack API errors"""
    mock_slack.return_value.chat_postMessage.side_effect = \
        Exception("API error")
    
    agent = CommsAgent()
    result = agent.run("slack", "Test message")
    assert result == ""

def test_email_success(setup_env, mock_smtp):
    """Should send email successfully"""
    agent = CommsAgent()
    result = agent.run("email", "Test message")
    assert "Email sent successfully" in result
    
    # Verify SMTP client called correctly
    mock_smtp.assert_called_once_with('smtp.test.com', 587)
    smtp = mock_smtp.return_value.__enter__.return_value
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once_with('test@test.com', 'test_pass')
    smtp.sendmail.assert_called_once()

def test_email_no_config(mock_smtp):
    """Should fail when email config not set"""
    agent = CommsAgent()
    result = agent.run("email", "Test message")
    assert result == ""
    
    # Verify SMTP client not called
    mock_smtp.assert_not_called()

def test_email_smtp_error(setup_env, mock_smtp):
    """Should handle SMTP errors"""
    mock_smtp.return_value.__enter__.return_value.sendmail.side_effect = \
        Exception("SMTP error")
    
    agent = CommsAgent()
    result = agent.run("email", "Test message")
    assert result == ""

def test_handle_communication_email_success(setup_env, mock_smtp):
    """Should handle email communication successfully"""
    assert handle_communication("email", "Test message")

def test_handle_communication_invalid_method():
    """Should handle invalid communication method"""
    assert not handle_communication("invalid", "Test message")

def test_handle_communication_error():
    """Should handle communication errors"""
    def mock_run(*args, **kwargs):
        raise Exception("Test error")
    
    with patch('ruv_cli.commands.agent.comms_agent.CommsAgent.run', 
              side_effect=mock_run):
        assert not handle_communication("email", "Test message")

@pytest.mark.skipif(not SLACK_AVAILABLE, reason="Slack SDK not installed")
def test_handle_communication_slack_success(setup_env, mock_slack):
    """Should handle Slack communication successfully"""
    assert handle_communication("slack", "Test message")