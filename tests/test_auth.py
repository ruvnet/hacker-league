import os
import json
import pytest
from pathlib import Path
from ruv_cli.commands import auth

@pytest.fixture
def cleanup_config():
    """Clean up config file before and after tests"""
    if auth.CONFIG_FILE.exists():
        auth.CONFIG_FILE.unlink()
    if auth.CONFIG_DIR.exists():
        auth.CONFIG_DIR.rmdir()
    yield
    if auth.CONFIG_FILE.exists():
        auth.CONFIG_FILE.unlink()
    if auth.CONFIG_DIR.exists():
        auth.CONFIG_DIR.rmdir()

def test_login_without_api_key(cleanup_config):
    """Should fail when E2B_API_KEY is not set"""
    if "E2B_API_KEY" in os.environ:
        del os.environ["E2B_API_KEY"]
    assert not auth.login()
    assert not auth.CONFIG_FILE.exists()

def test_login_with_api_key(cleanup_config):
    """Should succeed when E2B_API_KEY is set"""
    os.environ["E2B_API_KEY"] = "test_key"
    assert auth.login()
    assert auth.CONFIG_FILE.exists()
    
    # Verify stored config
    with open(auth.CONFIG_FILE) as f:
        config = json.load(f)
        assert config["api_key"] == "test_key"

def test_login_creates_config_dir(cleanup_config):
    """Should create config directory if it doesn't exist"""
    os.environ["E2B_API_KEY"] = "test_key"
    assert not auth.CONFIG_DIR.exists()
    assert auth.login()
    assert auth.CONFIG_DIR.exists()
    assert auth.CONFIG_FILE.exists()

def test_login_overwrites_existing_config(cleanup_config):
    """Should overwrite existing config file"""
    # First login
    os.environ["E2B_API_KEY"] = "first_key"
    auth.login()
    
    # Second login with different key
    os.environ["E2B_API_KEY"] = "second_key"
    assert auth.login()
    
    with open(auth.CONFIG_FILE) as f:
        config = json.load(f)
        assert config["api_key"] == "second_key"

def test_logout_with_config(cleanup_config):
    """Should remove config file when it exists"""
    # Setup: Create config file
    auth.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    auth.CONFIG_FILE.touch()
    
    assert auth.logout()
    assert not auth.CONFIG_FILE.exists()

def test_logout_without_config(cleanup_config):
    """Should handle case when no config exists"""
    assert not auth.CONFIG_FILE.exists()
    assert not auth.logout()

def test_login_handles_write_error(cleanup_config, monkeypatch):
    """Should handle errors when writing config file"""
    def mock_json_dump(*args, **kwargs):
        raise IOError("Write error")
    
    monkeypatch.setattr(json, "dump", mock_json_dump)
    os.environ["E2B_API_KEY"] = "test_key"
    
    assert not auth.login()
    assert not auth.CONFIG_FILE.exists()

def test_logout_handles_unlink_error(cleanup_config, monkeypatch):
    """Should handle errors when removing config file"""
    def mock_unlink(*args, **kwargs):
        raise IOError("Unlink error")
    
    # Setup: Create config file
    auth.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    auth.CONFIG_FILE.touch()
    
    monkeypatch.setattr(Path, "unlink", mock_unlink)
    assert not auth.logout()