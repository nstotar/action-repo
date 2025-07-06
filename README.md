# GitHub Webhook MongoDB Integration

This project implements a comprehensive GitHub webhook system that automatically receives push and pull request events, stores repository data in MongoDB, and displays changes in real-time with 15-second polling intervals.

## 🚀 Features

- **Multi-Event Support**: Handles GitHub push and pull request webhooks
- **MongoDB Integration**: Stores repository data with comprehensive schema
- **Real-time Display**: Polls MongoDB every 15 seconds to show changes
- **Data Validation**: Validates webhook payloads and data integrity
- **Health Monitoring**: Built-in health checks and error handling
- **Testing Suite**: Comprehensive testing framework for validation
- **Action Repository**: Sample repository with GitHub Actions workflow

## 📋 Requirements

- Python 3.7+
- MongoDB 4.0+
- Node.js 14+ (for action-repo testing)
- Git

## 🛠️ Quick Setup

### Automated Setup
```bash
# Clone and setup everything automatically
python setup.py
```

### Manual Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies (for action-repo):**
   ```bash
   cd action-repo
   npm install
   cd ..
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and configurations
   ```

4. **Start MongoDB:**
   ```bash
   mongod
   ```

## 🏃‍♂️ Running the System

### Option 1: Start Both Systems Together
```bash
python start_system.py
```

### Option 2: Start Systems Separately

**Terminal 1 - Webhook Receiver:**
```bash
python webhook_receiver.py
```

**Terminal 2 - Data Display:**
```bash
python data_display.py
```

## 🧪 Testing

### Complete System Test
```bash
python test_system.py
```

### Manual Webhook Testing
```bash
cd action-repo
npm run webhook-test
# Or with custom parameters:
node webhook-test.js http://localhost:5000/webhook push
node webhook-test.js http://localhost:5000/webhook pull_request
```

## 📊 MongoDB Schema

The system stores repository data with the following structure:

```json
{
  "author": "john_doe",
  "pushed_to": "repository:branch",
  "on": "2023-04-15T10:30:00Z",
  "timestamp": "2023-04-15T10:30:15.123Z",
  "sample": "Commit message or PR description"
}
```

### Field Descriptions:
- **`author`**: GitHub username who triggered the event
- **`pushed_to`**: Format: `repository:branch` (e.g., "myrepo:main")
- **`on`**: Original timestamp from GitHub event
- **`timestamp`**: Internal processing timestamp
- **`sample`**: Commit message, PR title, or event description

## 🔗 API Endpoints

- **Webhook Receiver**: `POST http://localhost:5000/webhook`
- **Health Check**: `GET http://localhost:5000/health`
- **Recent Data**: `GET http://localhost:5000/recent?limit=10`

## ⚙️ GitHub Webhook Configuration

1. Go to your repository **Settings > Webhooks**
2. Click **Add webhook**
3. Set **Payload URL**: `http://your-server:5000/webhook`
4. Set **Content type**: `application/json`
5. Select events: **Push** and **Pull requests**
6. Add **Secret** (optional but recommended)
7. Click **Add webhook**

## 📁 Project Structure

```
├── models/
│   ├── __init__.py
│   └── repository_data.py      # MongoDB data models
├── database/
│   ├── __init__.py
│   └── connection.py           # MongoDB connection management
├── action-repo/
│   ├── .github/workflows/
│   │   └── webhook-trigger.yml # GitHub Actions workflow
│   ├── package.json
│   ├── index.js
│   ├── webhook-test.js         # Webhook testing utility
│   └── README.md
├── webhook_receiver.py         # Flask webhook receiver
├── data_display.py            # Data polling and display system
├── start_system.py            # System startup script
├── test_system.py             # Comprehensive testing suite
├── setup.py                   # Automated setup script
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
├── .env.example              # Environment configuration template
└── README.md                 # This file
```

## 🔍 Data Display Format

The system displays repository changes in the following format:

```
============================================================
Repository Data Update - 2023-04-15 10:30:15 UTC
============================================================
Author: john_doe
Pushed to: myrepo:main
On: 15 Apr 2023 - 10:30 UTC
Sample: Added new authentication feature
----------------------------------------
Author: jane_smith
Pushed to: myrepo:develop
On: 15 Apr 2023 - 09:45 UTC
Sample: PR #42: Fix user login bug (opened)
----------------------------------------
Total records: 2
============================================================
```

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Failed:**
```bash
# Check if MongoDB is running
mongod --version
# Start MongoDB
mongod
```

**Port Already in Use:**
```bash
# Change port in .env file
FLASK_PORT=5001
```

**Webhook Not Receiving Data:**
- Check firewall settings
- Verify webhook URL is accessible
- Check GitHub webhook delivery logs
- Ensure webhook secret matches (if used)

**Missing Dependencies:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
cd action-repo && npm install
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/github_webhook_db
MONGODB_DATABASE=github_webhook_db
MONGODB_COLLECTION=repository_data

# Flask Configuration
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
FLASK_DEBUG=True

# GitHub Webhook Configuration
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
```

## 📈 Monitoring and Logs

- **Health Check**: Monitor system status at `http://localhost:5000/health`
- **Recent Data API**: View recent entries at `http://localhost:5000/recent`
- **Console Logs**: Both webhook receiver and data display provide detailed console output
- **Error Handling**: Comprehensive error handling with descriptive messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `python test_system.py`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run the system test: `python test_system.py`
3. Check MongoDB and Flask logs
4. Verify GitHub webhook configuration
5. Test with the provided webhook testing utility
