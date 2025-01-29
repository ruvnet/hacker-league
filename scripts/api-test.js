#!/usr/bin/env node
const https = require('https');

// Test Copilot API connectivity
async function testCopilotAPI() {
    try {
        console.log('🔍 Testing GitHub Copilot API connectivity...');
        
        // Get the token from environment or GitHub CLI
        const token = process.env.GITHUB_TOKEN || await getGitHubToken();
        
        if (!token) {
            throw new Error('No GitHub token available');
        }

        const data = JSON.stringify({
            messages: [
                { role: "user", content: "Write a function that adds two numbers" }
            ]
        });

        const options = {
            hostname: 'api.githubcopilot.com',
            path: '/chat/completions',
            method: 'POST',
            headers: {
                'X-Github-Token': token,
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        const response = await new Promise((resolve, reject) => {
            const req = https.request(options, (res) => {
                let responseData = '';
                
                res.on('data', (chunk) => {
                    responseData += chunk;
                });
                
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        resolve({
                            status: res.statusCode,
                            headers: res.headers,
                            body: responseData
                        });
                    } else {
                        reject(new Error(`API Error: ${res.statusCode} - ${responseData}`));
                    }
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            req.write(data);
            req.end();
        });

        console.log('✅ API Connection successful!');
        console.log('   Status:', response.status);
        console.log('   Response:', response.body.substring(0, 100) + '...');
        return true;

    } catch (error) {
        console.error('❌ API Test Failed:', error.message);
        if (error.message.includes('401')) {
            console.log('\n⚠️  Authentication Error:');
            console.log('   1. Ensure GITHUB_TOKEN is unset: unset GITHUB_TOKEN');
            console.log('   2. Refresh Copilot auth: gh auth refresh --hostname github.com --scopes copilot');
        }
        return false;
    }
}

// Helper function to get GitHub token from CLI if needed
async function getGitHubToken() {
    try {
        const { execSync } = require('child_process');
        const token = execSync('gh auth token').toString().trim();
        return token;
    } catch (error) {
        console.error('Failed to get GitHub token:', error.message);
        return null;
    }
}

// Run the test if executed directly
if (require.main === module) {
    testCopilotAPI();
}

module.exports = testCopilotAPI;
