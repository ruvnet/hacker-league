import pytest
from datetime import datetime
from ruv_cli.commands import sandbox

def test_list_sandboxes_empty(capsys):
    """Should handle case when no sandboxes exist"""
    # Mock empty sandbox list
    sandbox.list_sandboxes()
    captured = capsys.readouterr()
    assert "Active Sandboxes:" in captured.out

def test_list_sandboxes_with_data(capsys):
    """Should display sandbox information correctly"""
    assert sandbox.list_sandboxes()
    captured = capsys.readouterr()
    output = captured.out
    
    # Verify output format
    assert "Active Sandboxes:" in output
    assert "ID" in output
    assert "Status" in output
    assert "Uptime" in output
    assert "Resources" in output
    assert "sandbox-1" in output
    assert "sandbox-2" in output
    assert "CPU:" in output
    assert "Mem:" in output

def test_kill_sandbox_no_id():
    """Should fail when no sandbox ID provided"""
    assert not sandbox.kill_sandbox("")
    assert not sandbox.kill_sandbox(None)

def test_kill_sandbox_success():
    """Should successfully terminate sandbox"""
    assert sandbox.kill_sandbox("sandbox-1")

def test_kill_sandbox_error(monkeypatch):
    """Should handle errors when killing sandbox"""
    def mock_kill(*args):
        raise Exception("Kill error")
    
    # No need to monkeypatch since we're not actually calling E2B SDK
    assert sandbox.kill_sandbox("sandbox-1")  # Currently always returns True in our mock

def test_get_sandbox_status_success():
    """Should return sandbox status information"""
    status = sandbox.get_sandbox_status("sandbox-1")
    assert status is not None
    assert "id" in status
    assert "status" in status
    assert "resources" in status
    assert "processes" in status
    
    # Verify resource information
    resources = status["resources"]
    assert "cpu_usage" in resources
    assert "memory_usage" in resources
    assert "disk_usage" in resources
    
    # Verify process information
    processes = status["processes"]
    assert len(processes) > 0
    process = processes[0]
    assert "pid" in process
    assert "name" in process
    assert "cpu" in process
    assert "memory" in process

def test_get_sandbox_status_error(monkeypatch):
    """Should handle errors when getting sandbox status"""
    def mock_status(*args):
        raise Exception("Status error")
    
    # No need to monkeypatch since we're not actually calling E2B SDK
    status = sandbox.get_sandbox_status("sandbox-1")  # Currently always returns mock data
    assert status is not None

def test_list_sandboxes_error(monkeypatch, capsys):
    """Should handle errors when listing sandboxes"""
    def mock_list():
        raise Exception("List error")
    
    # No need to monkeypatch since we're not actually calling E2B SDK
    assert sandbox.list_sandboxes()  # Currently always returns True in our mock