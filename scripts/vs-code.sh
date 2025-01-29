#!/bin/bash

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed"
        if [ "$1" = "node" ]; then
            echo "   Hint: Install Node.js using nvm: nvm install node"
        fi
        return 1
    else
        echo "✅ $1 is installed ($(command -v $1))"
        return 0
    fi
}

# Function to check GitHub authentication status
check_github_auth() {
    if gh auth status &> /dev/null; then
        echo "✅ GitHub CLI is authenticated"
        return 0
    else
        echo "❌ GitHub CLI is not authenticated"
        echo "   Hint: Run 'gh auth login' to authenticate"
        return 1
    fi
}

# Function to check if VS Code extension is installed
check_vscode_extension() {
    if code --list-extensions 2>/dev/null | grep -q "^$1$"; then
        echo "✅ VS Code extension $1 is installed"
        return 0
    else
        echo "❌ VS Code extension $1 is not installed"
        if [ "$1" = "github.copilot" ]; then
            echo "   Hint: Install with:"
            echo "   1. Open VS Code"
            echo "   2. Press Ctrl+P"
            echo "   3. Type 'ext install github.copilot'"
            echo "   4. Click Install"
        else
            echo "   Hint: Install with 'code --install-extension $1'"
        fi
        return 1
    fi
}

# Function to run API connectivity test
run_api_test() {
    echo
    echo "🧪 Testing GitHub Copilot API..."
    chmod +x scripts/api-test.sh 2>/dev/null
    
    if [ -f "scripts/api-test.sh" ]; then
        ./scripts/api-test.sh
        return $?
    else
        echo "❌ API test script not found (scripts/api-test.sh)"
        return 1
    fi
}

echo "🔍 Checking required dependencies..."
FAILED=0

# Check core dependencies
DEPS=(curl git node npm code gh)
for dep in "${DEPS[@]}"; do
    check_command $dep || FAILED=$((FAILED + 1))
done

# Check GitHub auth status
check_github_auth || FAILED=$((FAILED + 1))

# Check VS Code Copilot extension
check_vscode_extension "github.copilot" || FAILED=$((FAILED + 1))

echo
if [ $FAILED -eq 0 ]; then
    echo "✨ Base requirements satisfied!"
    run_api_test
else
    echo "❌ $FAILED requirement(s) not satisfied"
    echo "Please review the installation hints above for missing dependencies"
    exit 1
fi
