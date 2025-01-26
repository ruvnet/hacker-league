# Auth Command Implementation Guide

## Directory Structure

```plaintext
src/ruv_cli/
├── __init__.py
├── cli.py
└── commands/
    ├── __init__.py
    └── auth.py
```

## Implementation Steps

### 1. Basic Package Setup

#### __init__.py
```python
# src/ruv_cli/__init__.py
__version__ = "0.1.0"
```

#### cli.py
```python
# src/ruv_cli/cli.py
import argparse
import sys
from .commands import auth

def main():
    parser = argparse.ArgumentParser(
        prog="ruv",
        description="RUV CLI - E2B Agent Management"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Auth subcommand
    auth_parser = subparsers.add_parser("auth", help="Authentication commands")
    auth_sub = auth_parser.add_subparsers(dest="auth_cmd")
    auth_sub.add_parser("login", help="Login to E2B")
    auth_sub.add_parser("logout", help="Logout from E2B")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    if args.command == "auth":
        if args.auth_cmd == "login":
            auth.login()
        elif args.auth_cmd == "logout":
            auth.logout()
        else:
            auth_parser.print_help()
            sys.exit(1)

if __name__ == "__main__":
    main()
```

#### auth.py
```python
# src/ruv_cli/commands/auth.py
import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".ruv"
CONFIG_FILE = CONFIG_DIR / "config.json"

def login():
    """Login to E2B using API key from environment"""
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        print("Error: E2B_API_KEY environment variable not set")
        return False
        
    # Create config directory if it doesn't exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Store API key
    config = {"api_key": api_key}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
        
    print("Successfully logged in to E2B")
    return True

def logout():
    """Clear stored credentials"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        print("Successfully logged out from E2B")
        return True
    
    print("No active session found")
    return False
```

## Test Implementation

### test_auth.py
```python
# tests/test_auth.py
import os
import pytest
from pathlib import Path
from ruv_cli.commands import auth

def test_login_without_api_key():
    """Should fail when E2B_API_KEY is not set"""
    if "E2B_API_KEY" in os.environ:
        del os.environ["E2B_API_KEY"]
    assert not auth.login()

def test_login_with_api_key():
    """Should succeed when E2B_API_KEY is set"""
    os.environ["E2B_API_KEY"] = "test_key"
    assert auth.login()
    assert auth.CONFIG_FILE.exists()
    
def test_logout():
    """Should clear stored credentials"""
    auth.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    auth.CONFIG_FILE.touch()
    assert auth.logout()
    assert not auth.CONFIG_FILE.exists()

def test_logout_without_session():
    """Should handle case when no session exists"""
    if auth.CONFIG_FILE.exists():
        auth.CONFIG_FILE.unlink()
    assert not auth.logout()
```

## Testing Steps

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install pytest
```

3. Set environment variables:
```bash
export E2B_API_KEY=your_test_key
```

4. Run tests:
```bash
pytest tests/test_auth.py -v
```

## Expected Test Results

```
test_auth.py::test_login_without_api_key PASSED
test_auth.py::test_login_with_api_key PASSED
test_auth.py::test_logout PASSED
test_auth.py::test_logout_without_session PASSED
```

## Manual Testing

1. Login:
```bash
python -m ruv_cli auth login
# Expected: "Successfully logged in to E2B"
```

2. Logout:
```bash
python -m ruv_cli auth logout
# Expected: "Successfully logged out from E2B"
```

## Next Steps

1. Switch to Code mode to implement the actual code
2. Create the directory structure
3. Implement the auth command
4. Create and run tests
5. Verify functionality