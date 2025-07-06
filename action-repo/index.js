/**
 * GitHub Actions Repository - Main Entry Point
 * This file serves as the main entry point for the action-repo
 */

console.log('🚀 GitHub Actions Repository - nstotar/action-repo');
console.log('📊 Repository configured for webhook testing');
console.log('🔗 Integration with GitHub Webhook MongoDB System');

// Display repository information
const repoInfo = {
    name: 'action-repo',
    owner: 'nstotar',
    purpose: 'GitHub webhook testing and MongoDB integration',
    features: [
        'GitHub Actions workflows',
        'Webhook testing utilities',
        'MongoDB integration support',
        'Real-time data monitoring'
    ]
};

console.log('\n📋 Repository Information:');
console.log(`   Name: ${repoInfo.name}`);
console.log(`   Owner: ${repoInfo.owner}`);
console.log(`   Purpose: ${repoInfo.purpose}`);
console.log('\n✨ Features:');
repoInfo.features.forEach(feature => {
    console.log(`   • ${feature}`);
});

console.log('\n🔧 Usage:');
console.log('   npm run webhook-test  - Test webhook functionality');
console.log('   npm start            - Run this information script');

console.log('\n🌐 Webhook Integration:');
console.log('   Configure GitHub webhooks to point to your webhook receiver');
console.log('   Default endpoint: http://localhost:5000/webhook');

console.log('\n✅ Repository ready for GitHub Actions and webhook testing!');
