import sys
import pytest
from unittest.mock import patch
from ruv_cli import cli
from ruv_cli.commands import auth, template, sandbox, agent

def test_main_no_args(capsys):
    """Should show help when no arguments provided"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv']):
            cli.main()
    
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "RUV CLI - E2B Agent Management" in captured.out
    assert "auth" in captured.out
    assert "template" in captured.out
    assert "sandbox" in captured.out
    assert "agent" in captured.out

def test_auth_no_subcommand(capsys):
    """Should show auth help when no subcommand provided"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'auth']):
            cli.main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Authentication commands" in captured.out
    assert "login" in captured.out
    assert "logout" in captured.out

def test_auth_login_success():
    """Should exit with 0 on successful login"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'auth', 'login']):
            with patch.object(auth, 'login', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_auth_login_failure():
    """Should exit with 1 on failed login"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'auth', 'login']):
            with patch.object(auth, 'login', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_auth_logout_success():
    """Should exit with 0 on successful logout"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'auth', 'logout']):
            with patch.object(auth, 'logout', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_auth_logout_failure():
    """Should exit with 1 on failed logout"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'auth', 'logout']):
            with patch.object(auth, 'logout', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_template_no_subcommand(capsys):
    """Should show template help when no subcommand provided"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template']):
            cli.main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Template commands" in captured.out
    assert "init" in captured.out
    assert "build" in captured.out
    assert "list" in captured.out

def test_template_init_success():
    """Should exit with 0 on successful template init"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template', 'init']):
            with patch.object(template, 'init_template', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_template_init_failure():
    """Should exit with 1 on failed template init"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template', 'init']):
            with patch.object(template, 'init_template', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_template_build_success():
    """Should exit with 0 on successful template build"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template', 'build']):
            with patch.object(template, 'build_template', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_template_build_failure():
    """Should exit with 1 on failed template build"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template', 'build']):
            with patch.object(template, 'build_template', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_template_list_success():
    """Should exit with 0 on successful template list"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template', 'list']):
            with patch.object(template, 'list_templates', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_template_list_failure():
    """Should exit with 1 on failed template list"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'template', 'list']):
            with patch.object(template, 'list_templates', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_sandbox_no_subcommand(capsys):
    """Should show sandbox help when no subcommand provided"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox']):
            cli.main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Sandbox commands" in captured.out
    assert "list" in captured.out
    assert "kill" in captured.out
    assert "status" in captured.out

def test_sandbox_list_success():
    """Should exit with 0 on successful sandbox list"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox', 'list']):
            with patch.object(sandbox, 'list_sandboxes', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_sandbox_list_failure():
    """Should exit with 1 on failed sandbox list"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox', 'list']):
            with patch.object(sandbox, 'list_sandboxes', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_sandbox_kill_success():
    """Should exit with 0 on successful sandbox kill"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox', 'kill', 'sandbox-1']):
            with patch.object(sandbox, 'kill_sandbox', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_sandbox_kill_failure():
    """Should exit with 1 on failed sandbox kill"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox', 'kill', 'sandbox-1']):
            with patch.object(sandbox, 'kill_sandbox', return_value=False):
                cli.main()
    
    assert e.value.code == 1

def test_sandbox_status_success():
    """Should exit with 0 on successful sandbox status"""
    mock_status = {
        'id': 'sandbox-1',
        'status': 'running',
        'started': '2023-01-01',
        'resources': {'cpu': '10%'},
        'processes': []
    }
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox', 'status', 'sandbox-1']):
            with patch.object(sandbox, 'get_sandbox_status', return_value=mock_status):
                cli.main()
    
    assert e.value.code == 0

def test_sandbox_status_failure():
    """Should exit with 1 on failed sandbox status"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'sandbox', 'status', 'sandbox-1']):
            with patch.object(sandbox, 'get_sandbox_status', return_value=None):
                cli.main()
    
    assert e.value.code == 1

def test_agent_no_subcommand(capsys):
    """Should show agent help when no subcommand provided"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'agent']):
            cli.main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Agent commands" in captured.out
    assert "code" in captured.out
    assert "data" in captured.out
    assert "employee" in captured.out
    assert "comms" in captured.out

def test_agent_code_success():
    """Should exit with 0 on successful code generation"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'agent', 'code', 'print hello']):
            with patch.object(agent, 'handle_agent_command', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_agent_data_success():
    """Should exit with 0 on successful data operation"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'agent', 'data', 'describe', '--file=data.csv']):
            with patch.object(agent, 'handle_agent_command', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_agent_employee_success():
    """Should exit with 0 on successful employee operation"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'agent', 'employee', 'analyst', '--start']):
            with patch.object(agent, 'handle_agent_command', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_agent_comms_success():
    """Should exit with 0 on successful communication"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'agent', 'comms', 'slack', '--message=test']):
            with patch.object(agent, 'handle_agent_command', return_value=True):
                cli.main()
    
    assert e.value.code == 0

def test_invalid_command(capsys):
    """Should show help on invalid command"""
    with pytest.raises(SystemExit) as e:
        with patch.object(sys, 'argv', ['ruv', 'invalid']):
            cli.main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "invalid choice: 'invalid'" in captured.err