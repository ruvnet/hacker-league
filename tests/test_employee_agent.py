import time
import pytest
from unittest.mock import patch
from ruv_cli.commands.agent.employee_agent import (
    EmployeeAgent,
    manage_employee_agent,
    AGENT_THREADS,
    AGENT_STATES,
    ROLE_TO_ID
)

@pytest.fixture(autouse=True)
def cleanup_agents():
    """Clean up any running agents before and after tests"""
    AGENT_THREADS.clear()
    AGENT_STATES.clear()
    ROLE_TO_ID.clear()
    yield
    # Stop all agents
    for agent_id in list(AGENT_STATES.keys()):
        AGENT_STATES[agent_id] = False
    # Wait for threads to stop
    threads = list(AGENT_THREADS.values())  # Create a copy of values
    for thread in threads:
        thread.join(timeout=1.0)
    AGENT_THREADS.clear()
    AGENT_STATES.clear()
    ROLE_TO_ID.clear()

def wait_for_thread_cleanup(prefix: str, timeout: float = 1.0):
    """Wait for threads with given prefix to be cleaned up"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        agent_ids = [k for k in AGENT_THREADS.keys() if k.startswith(prefix)]
        if not agent_ids:
            return True
        time.sleep(0.1)
    return False

def test_employee_agent_initialization():
    """Should initialize with role"""
    agent = EmployeeAgent(role="analyst")
    assert agent.name == "EmployeeAgent"
    assert agent.role == "analyst"
    
    agent = EmployeeAgent(name="CustomAgent", role="engineer")
    assert agent.name == "CustomAgent"
    assert agent.role == "engineer"

def test_employee_agent_start():
    """Should start agent thread"""
    agent = EmployeeAgent(role="analyst")
    result = agent.run(start=True)
    assert "Started agent analyst" in result
    
    # Verify thread is running
    agent_id = f"analyst_{id(agent)}"
    assert agent_id in AGENT_THREADS
    assert AGENT_THREADS[agent_id].is_alive()
    assert AGENT_STATES[agent_id]
    assert ROLE_TO_ID["analyst"] == agent_id

def test_employee_agent_stop():
    """Should stop agent thread"""
    agent = EmployeeAgent(role="analyst")
    agent.run(start=True)
    
    result = agent.run(stop=True)
    assert "Stopped agent analyst" in result
    
    # Verify thread is stopped
    assert "analyst" not in ROLE_TO_ID
    assert wait_for_thread_cleanup("analyst")

def test_employee_agent_status():
    """Should report agent status"""
    agent = EmployeeAgent(role="analyst")
    
    # Not running
    result = agent.run(status=True)
    assert "not running" in result
    
    # Running
    agent.run(start=True)
    result = agent.run(status=True)
    assert "is running" in result

def test_employee_agent_start_already_running():
    """Should handle starting already running agent"""
    agent = EmployeeAgent(role="analyst")
    agent.run(start=True)
    
    result = agent.run(start=True)
    assert "already running" in result

def test_employee_agent_stop_not_running():
    """Should handle stopping non-running agent"""
    agent = EmployeeAgent(role="analyst")
    result = agent.run(stop=True)
    assert "not running" in result

def test_employee_agent_invalid_operation():
    """Should fail with no operation specified"""
    agent = EmployeeAgent(role="analyst")
    result = agent.run()
    assert result == ""

def test_manage_employee_no_role():
    """Should fail when no role provided"""
    assert not manage_employee_agent("")

def test_manage_employee_start():
    """Should start employee agent"""
    assert manage_employee_agent("analyst", start=True)
    
    # Verify agent is running
    assert "analyst" in ROLE_TO_ID
    agent_id = ROLE_TO_ID["analyst"]
    assert AGENT_THREADS[agent_id].is_alive()

def test_manage_employee_stop():
    """Should stop employee agent"""
    manage_employee_agent("analyst", start=True)
    time.sleep(0.1)  # Give thread time to start
    assert manage_employee_agent("analyst", stop=True)
    
    # Verify agent is stopped
    assert "analyst" not in ROLE_TO_ID
    assert wait_for_thread_cleanup("analyst")

def test_manage_employee_status():
    """Should report employee agent status"""
    assert manage_employee_agent("analyst", status=True)

def test_manage_employee_error():
    """Should handle operation errors"""
    def mock_run(*args, **kwargs):
        raise Exception("Test error")
    
    with patch('ruv_cli.commands.agent.employee_agent.EmployeeAgent.run', side_effect=mock_run):
        assert not manage_employee_agent("analyst", start=True)

def test_employee_agent_loop_error():
    """Should handle errors in agent loop"""
    class ErrorAgent(EmployeeAgent):
        def _run_loop(self, agent_id: str):
            self.log(f"Starting {self.role} loop")
            try:
                raise Exception("Test error")
            finally:
                if agent_id in AGENT_THREADS:
                    del AGENT_THREADS[agent_id]
                if agent_id in AGENT_STATES:
                    del AGENT_STATES[agent_id]
                if self.role in ROLE_TO_ID:
                    del ROLE_TO_ID[self.role]
                self.log(f"Stopping {self.role} loop")
    
    agent = ErrorAgent(role="analyst")
    agent.run(start=True)
    time.sleep(0.1)  # Give thread time to error
    
    # Verify agent handled error
    assert "analyst" not in ROLE_TO_ID
    assert wait_for_thread_cleanup("analyst")