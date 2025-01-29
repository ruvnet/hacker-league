#!/bin/bash

echo "🔍 Testing GitHub Copilot API connectivity..."

# Get the GitHub token from CLI if not provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "   Getting GitHub token from CLI..."
    GITHUB_TOKEN=$(gh auth token 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "❌ Failed to get GitHub token"
        echo "   Run: gh auth refresh --hostname github.com --scopes copilot"
        exit 1
    fi
fi

# Test the API with verbose output
echo "   Sending test request to Copilot API..."
echo "   Using token: ${GITHUB_TOKEN:0:6}...${GITHUB_TOKEN: -4}"

RESPONSE=$(curl -X POST "https://api.githubcopilot.com/chat/completions" \
    -H "X-Github-Token: ${GITHUB_TOKEN}" \
    -H "Content-Type: application/json" \
    -H "Editor-Version: vscode/1.85.1" \
    -H "Editor-Plugin-Version: copilot/1.138.0" \
    -H "Accept: application/json" \
    -d '{
        "messages": [
            {
                "role": "user",
                "content": "Write a hello world function"
            }
        ],
        "model": "gpt-4",
        "temperature": 0.1,
        "stream": false
    }' \
    -v \
    2>&1)

# Check if the response contains "HTTP/2 400"
if echo "$RESPONSE" > >(tee /dev/stderr) | grep -q "HTTP/2 400"; then
    echo "❌ API request failed with 400 Bad Request"
    echo "   Full response:"
    echo "$RESPONSE" | sed 's/^/   /'
    echo
    echo "💡 Try refreshing Copilot authentication:"
    echo "   1. gh auth refresh --hostname github.com --scopes copilot"
    echo "   2. Verify token with: gh auth status"
    exit 1
elif echo "$RESPONSE" | grep -q "HTTP/2 200"; then
    echo "✅ API connection successful!"
    echo "   Response received:"
    echo "$RESPONSE" | grep -v "^*" | sed 's/^/   /'
else
    echo "❌ API request failed"
    echo "   Error response:"
    echo "$RESPONSE" | sed 's/^/   /'
    if echo "$RESPONSE" | grep -q "401"; then
        echo
        echo "💡 Authentication error. Try:"
        echo "   1. gh auth refresh --hostname github.com --scopes copilot"
        echo "   2. Verify token with: gh auth status"
    fi
    exit 1
fi
