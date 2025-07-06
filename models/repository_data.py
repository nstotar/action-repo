"""
MongoDB model for repository data storage
"""
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class RepositoryDataModel:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.client[os.getenv('MONGODB_DATABASE', 'github_webhook_db')]
        self.collection = self.db[os.getenv('MONGODB_COLLECTION', 'repository_data')]
        
        # Create indexes for better performance
        self.collection.create_index([("timestamp", -1)])
        self.collection.create_index([("author", 1)])
        self.collection.create_index([("pushed_to", 1)])
    
    def insert_repository_data(self, data):
        """
        Insert repository data into MongoDB
        
        Expected data format:
        {
            "author": str,
            "pushed_to": str,
            "on": str (timestamp),
            "timestamp": datetime,
            "sample": str
        }
        """
        try:
            # Ensure timestamp is set
            if 'timestamp' not in data:
                data['timestamp'] = datetime.utcnow()
            
            # Validate required fields
            required_fields = ['author', 'pushed_to', 'on', 'sample']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f"Error inserting data: {e}")
            return None
    
    def get_recent_data(self, limit=50):
        """
        Get recent repository data sorted by timestamp
        """
        try:
            cursor = self.collection.find().sort("timestamp", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
    
    def get_data_since(self, since_timestamp):
        """
        Get data since a specific timestamp
        """
        try:
            cursor = self.collection.find({
                "timestamp": {"$gt": since_timestamp}
            }).sort("timestamp", -1)
            return list(cursor)
        except Exception as e:
            print(f"Error fetching data since timestamp: {e}")
            return []
    
    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()

# Schema validation function
def validate_repository_data(data):
    """
    Validate repository data against expected schema
    """
    required_fields = {
        'author': str,
        'pushed_to': str,
        'on': str,
        'sample': str
    }
    
    for field, expected_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], expected_type):
            return False, f"Field {field} must be of type {expected_type.__name__}"
    
    return True, "Valid"

# Sample data structure for reference
SAMPLE_REPOSITORY_DATA = {
    "author": "john_doe",
    "pushed_to": "main",
    "on": "2023-04-15T10:30:00Z",
    "timestamp": datetime.utcnow(),
    "sample": "Added new feature for user authentication"
}
