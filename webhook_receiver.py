"""
GitHub Webhook Receiver
Handles incoming GitHub webhook events and stores data in MongoDB
"""
from flask import Flask, request, jsonify
import json
import hashlib
import hmac
import os
from datetime import datetime
from dotenv import load_dotenv
from models.repository_data import RepositoryDataModel, validate_repository_data

load_dotenv()

app = Flask(__name__)

# Initialize MongoDB model
repo_model = RepositoryDataModel()

def verify_signature(payload_body, signature_header):
    """Verify GitHub webhook signature"""
    if not signature_header:
        return False
    
    secret = os.getenv('GITHUB_WEBHOOK_SECRET', '')
    if not secret:
        return True  # Skip verification if no secret is set
    
    hash_object = hmac.new(
        secret.encode('utf-8'),
        payload_body,
        hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

def extract_push_data(payload):
    """Extract relevant data from GitHub push payload"""
    try:
        # Extract author information
        author = payload.get('pusher', {}).get('name', 'unknown')
        if not author or author == 'unknown':
            author = payload.get('head_commit', {}).get('author', {}).get('name', 'unknown')
        
        # Extract repository and branch information
        repository = payload.get('repository', {}).get('name', 'unknown')
        ref = payload.get('ref', 'refs/heads/main')
        branch = ref.split('/')[-1] if ref.startswith('refs/heads/') else ref
        pushed_to = f"{repository}:{branch}"
        
        # Extract timestamp
        timestamp_str = payload.get('head_commit', {}).get('timestamp')
        if not timestamp_str:
            timestamp_str = datetime.utcnow().isoformat() + 'Z'
        
        # Extract commit message as sample
        sample = payload.get('head_commit', {}).get('message', 'No commit message')
        
        return {
            'author': author,
            'pushed_to': pushed_to,
            'on': timestamp_str,
            'timestamp': datetime.utcnow(),
            'sample': sample
        }
    except Exception as e:
        print(f"Error extracting push data: {e}")
        return None

def extract_pull_request_data(payload):
    """Extract relevant data from GitHub pull request payload"""
    try:
        action = payload.get('action', 'unknown')
        pr = payload.get('pull_request', {})
        
        author = pr.get('user', {}).get('login', 'unknown')
        repository = payload.get('repository', {}).get('name', 'unknown')
        base_branch = pr.get('base', {}).get('ref', 'main')
        head_branch = pr.get('head', {}).get('ref', 'unknown')
        
        pushed_to = f"{repository}:{base_branch}"
        
        # Use PR creation or update time
        timestamp_str = pr.get('created_at') or pr.get('updated_at')
        if not timestamp_str:
            timestamp_str = datetime.utcnow().isoformat() + 'Z'
        
        sample = f"PR #{pr.get('number', 'unknown')}: {pr.get('title', 'No title')} ({action})"
        
        return {
            'author': author,
            'pushed_to': pushed_to,
            'on': timestamp_str,
            'timestamp': datetime.utcnow(),
            'sample': sample
        }
    except Exception as e:
        print(f"Error extracting pull request data: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming GitHub webhook"""
    try:
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256')
        if not verify_signature(request.data, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Get event type
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        if not payload:
            return jsonify({'error': 'No payload received'}), 400
        
        # Process different event types
        data = None
        if event_type == 'push':
            data = extract_push_data(payload)
        elif event_type == 'pull_request':
            data = extract_pull_request_data(payload)
        else:
            print(f"Unsupported event type: {event_type}")
            return jsonify({'message': f'Event type {event_type} not supported'}), 200
        
        if not data:
            return jsonify({'error': 'Failed to extract data from payload'}), 400
        
        # Validate data
        is_valid, message = validate_repository_data(data)
        if not is_valid:
            return jsonify({'error': f'Invalid data: {message}'}), 400
        
        # Store in MongoDB
        result_id = repo_model.insert_repository_data(data)
        if result_id:
            print(f"Successfully stored data with ID: {result_id}")
            print(f"Data: {data}")
            return jsonify({
                'message': 'Webhook processed successfully',
                'id': str(result_id),
                'event_type': event_type
            }), 200
        else:
            return jsonify({'error': 'Failed to store data'}), 500
            
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/recent', methods=['GET'])
def get_recent_data():
    """Get recent repository data for testing"""
    try:
        limit = request.args.get('limit', 10, type=int)
        data = repo_model.get_recent_data(limit)
        
        # Convert ObjectId to string for JSON serialization
        for item in data:
            item['_id'] = str(item['_id'])
            if 'timestamp' in item:
                item['timestamp'] = item['timestamp'].isoformat()
        
        return jsonify({'data': data, 'count': len(data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting webhook receiver on {host}:{port}")
    print(f"Webhook endpoint: http://{host}:{port}/webhook")
    print(f"Health check: http://{host}:{port}/health")
    
    app.run(host=host, port=port, debug=debug)
