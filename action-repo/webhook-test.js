/**
 * Webhook Testing Utility
 * Simulates GitHub webhook events for testing the webhook receiver
 */

const axios = require('axios');

// Default configuration
const DEFAULT_WEBHOOK_URL = 'http://localhost:5000/webhook';
const DEFAULT_EVENT_TYPE = 'push';

// Sample webhook payloads
const webhookPayloads = {
    push: {
        ref: 'refs/heads/main',
        before: '0000000000000000000000000000000000000000',
        after: 'a1b2c3d4e5f6789012345678901234567890abcd',
        repository: {
            id: 123456789,
            name: 'action-repo',
            full_name: 'nstotar/action-repo',
            owner: {
                name: 'nstotar',
                login: 'nstotar'
            },
            default_branch: 'main'
        },
        pusher: {
            name: 'nstotar',
            email: 'nstotar@example.com'
        },
        head_commit: {
            id: 'a1b2c3d4e5f6789012345678901234567890abcd',
            message: 'Add webhook integration features',
            timestamp: new Date().toISOString(),
            author: {
                name: 'nstotar',
                email: 'nstotar@example.com',
                username: 'nstotar'
            },
            committer: {
                name: 'nstotar',
                email: 'nstotar@example.com',
                username: 'nstotar'
            }
        },
        commits: [
            {
                id: 'a1b2c3d4e5f6789012345678901234567890abcd',
                message: 'Add webhook integration features',
                timestamp: new Date().toISOString(),
                author: {
                    name: 'nstotar',
                    email: 'nstotar@example.com',
                    username: 'nstotar'
                },
                committer: {
                    name: 'nstotar',
                    email: 'nstotar@example.com',
                    username: 'nstotar'
                }
            }
        ]
    },
    
    pull_request: {
        action: 'opened',
        number: 42,
        pull_request: {
            id: 987654321,
            number: 42,
            title: 'Add new webhook testing features',
            body: 'This PR adds comprehensive webhook testing capabilities to the action-repo.',
            state: 'open',
            user: {
                login: 'nstotar',
                id: 12345678
            },
            head: {
                ref: 'feature/webhook-testing',
                sha: 'b2c3d4e5f6789012345678901234567890abcde1',
                repo: {
                    name: 'action-repo',
                    full_name: 'nstotar/action-repo'
                }
            },
            base: {
                ref: 'main',
                sha: 'a1b2c3d4e5f6789012345678901234567890abcd',
                repo: {
                    name: 'action-repo',
                    full_name: 'nstotar/action-repo'
                }
            },
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        },
        repository: {
            id: 123456789,
            name: 'action-repo',
            full_name: 'nstotar/action-repo',
            owner: {
                login: 'nstotar'
            }
        },
        sender: {
            login: 'nstotar',
            id: 12345678
        }
    }
};

async function sendWebhook(url, eventType, payload) {
    try {
        console.log(`🚀 Sending ${eventType} webhook to ${url}`);
        console.log('📦 Payload preview:', JSON.stringify(payload, null, 2).substring(0, 200) + '...');
        
        const response = await axios.post(url, payload, {
            headers: {
                'Content-Type': 'application/json',
                'X-GitHub-Event': eventType,
                'X-GitHub-Delivery': `webhook-test-${Date.now()}`,
                'User-Agent': 'GitHub-Hookshot/webhook-test'
            },
            timeout: 10000
        });
        
        console.log('✅ Webhook sent successfully!');
        console.log(`   Status: ${response.status}`);
        console.log(`   Response: ${JSON.stringify(response.data)}`);
        
    } catch (error) {
        console.error('❌ Webhook failed:');
        if (error.response) {
            console.error(`   Status: ${error.response.status}`);
            console.error(`   Response: ${JSON.stringify(error.response.data)}`);
        } else if (error.request) {
            console.error('   No response received - is the webhook receiver running?');
            console.error('   Make sure to start the webhook receiver with: python webhook_receiver.py');
        } else {
            console.error(`   Error: ${error.message}`);
        }
    }
}

async function main() {
    const args = process.argv.slice(2);
    const webhookUrl = args[0] || DEFAULT_WEBHOOK_URL;
    const eventType = args[1] || DEFAULT_EVENT_TYPE;
    
    console.log('🧪 GitHub Webhook Test Utility');
    console.log('================================');
    console.log(`📡 Target URL: ${webhookUrl}`);
    console.log(`📋 Event Type: ${eventType}`);
    console.log('');
    
    if (!webhookPayloads[eventType]) {
        console.error(`❌ Unknown event type: ${eventType}`);
        console.log('Available event types:', Object.keys(webhookPayloads).join(', '));
        process.exit(1);
    }
    
    await sendWebhook(webhookUrl, eventType, webhookPayloads[eventType]);
}

// Run the test if this file is executed directly
if (require.main === module) {
    main().catch(console.error);
}

module.exports = { sendWebhook, webhookPayloads };
