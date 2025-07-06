# Action Repository - nstotar/action-repo

This is a GitHub Actions test repository for webhook integration with the GitHub Webhook MongoDB Integration system.

## 🚀 Features

- **GitHub Actions Workflow**: Automatically triggers on push/PR events
- **Webhook Testing**: Built-in webhook test utilities
- **MongoDB Integration**: Works with the webhook receiver system
- **Real-time Monitoring**: Integrates with the data display system

## 📋 Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Webhook URL
Edit `webhook-test.js` to point to your webhook receiver:
```javascript
const DEFAULT_WEBHOOK_URL = 'http://localhost:5000/webhook';
```

## 🔧 Usage

### Test Webhooks Locally
```bash
# Test push event
npm run webhook-test

# Test with custom parameters
node webhook-test.js http://localhost:5000/webhook push
node webhook-test.js http://localhost:5000/webhook pull_request
```

### GitHub Actions Workflow
The workflow automatically triggers on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to these branches
- Manual workflow dispatch

## 🔗 Integration with Main System

This repository works with the GitHub Webhook MongoDB Integration system:

1. **Start the main system** (in the parent directory):
   ```bash
   python start_system.py
   ```

2. **Configure GitHub Webhooks**:
   - Go to repository Settings > Webhooks
   - Add webhook URL: `http://your-server:5000/webhook`
   - Select events: Push, Pull requests
   - Content type: `application/json`

3. **Test the integration**:
   - Push changes to this repository
   - Watch the data display system show real-time updates
   - Check MongoDB for stored webhook data

## 📊 Webhook Data Format

When this repository triggers webhooks, the data is stored in MongoDB with this format:
```json
{
  "author": "nstotar",
  "pushed_to": "action-repo:main",
  "on": "2025-07-06T21:15:00Z",
  "timestamp": "2025-07-06T21:15:15.123Z",
  "sample": "Add webhook integration features"
}
```

## 🧪 Testing

The repository includes comprehensive testing capabilities:
- Local webhook testing with `webhook-test.js`
- GitHub Actions workflow validation
- Integration testing with the main system

## 📁 Files

- `.github/workflows/webhook-trigger.yml` - GitHub Actions workflow
- `webhook-test.js` - Local webhook testing utility
- `package.json` - Node.js dependencies and scripts
- `index.js` - Main application file
- `README.md` - This documentation

## 🚀 Quick Start

1. Clone this repository
2. Run `npm install`
3. Start the main webhook system: `python start_system.py`
4. Test webhooks: `npm run webhook-test`
5. Push changes to see real-time webhook processing

## 🔧 Configuration

### Environment Variables
You can set these in your GitHub repository secrets:
- `WEBHOOK_URL`: URL of your webhook receiver
- `WEBHOOK_SECRET`: Secret for webhook verification (optional)

### Local Testing
For local development, ensure the webhook receiver is running:
```bash
python webhook_receiver.py
```

Then test with:
```bash
npm run webhook-test
```
