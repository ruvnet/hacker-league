// Test script for GitHub Copilot API connectivity
const testCopilotAPI = async () => {
    try {
        console.log('🔍 Testing GitHub Copilot API connectivity...');
        const response = await fetch('https://api.githubcopilot.com/chat/completions', {
            method: 'POST',
            headers: {
                'X-Github-Token': process.env.GITHUB_TOKEN || 'local-env-token',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: [
                    { role: "user", content: "Write a simple hello world function" }
                ]
            })
        });

        const data = await response.json();
        console.log('✅ API Response:', data);
        return true;
    } catch (error) {
        console.error('❌ API Test Failed:', error.message);
        return false;
    }
};

// Run the test if executed directly
if (require.main === module) {
    testCopilotAPI();
}

module.exports = testCopilotAPI;
