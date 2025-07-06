"""
MongoDB connection management and utilities
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import time

load_dotenv()

class MongoDBConnection:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self, max_retries=3, retry_delay=2):
        """Establish connection to MongoDB with retry logic"""
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        for attempt in range(max_retries):
            try:
                print(f"Attempting to connect to MongoDB (attempt {attempt + 1}/{max_retries})")
                self._client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=5000,  # 5 second timeout
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000
                )
                
                # Test the connection
                self._client.admin.command('ping')
                print("Successfully connected to MongoDB")
                return True
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                print(f"Failed to connect to MongoDB: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Could not connect to MongoDB.")
                    return False
            except Exception as e:
                print(f"Unexpected error connecting to MongoDB: {e}")
                return False
        
        return False
    
    def get_client(self):
        """Get MongoDB client instance"""
        if self._client is None:
            self.connect()
        return self._client
    
    def get_database(self, db_name=None):
        """Get database instance"""
        if db_name is None:
            db_name = os.getenv('MONGODB_DATABASE', 'github_webhook_db')
        
        client = self.get_client()
        if client:
            return client[db_name]
        return None
    
    def get_collection(self, collection_name=None, db_name=None):
        """Get collection instance"""
        if collection_name is None:
            collection_name = os.getenv('MONGODB_COLLECTION', 'repository_data')
        
        db = self.get_database(db_name)
        if db:
            return db[collection_name]
        return None
    
    def test_connection(self):
        """Test MongoDB connection"""
        try:
            client = self.get_client()
            if client:
                client.admin.command('ping')
                return True
        except Exception as e:
            print(f"Connection test failed: {e}")
        return False
    
    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            print("MongoDB connection closed")

# Database initialization and setup
def initialize_database():
    """Initialize database with required indexes and collections"""
    try:
        connection = MongoDBConnection()
        collection = connection.get_collection()
        
        if collection is None:
            print("Failed to get collection")
            return False
        
        # Create indexes for better performance
        indexes = [
            [("timestamp", -1)],  # For time-based queries
            [("author", 1)],      # For author-based queries
            [("pushed_to", 1)],   # For repository-based queries
            [("on", -1)],         # For event time queries
        ]
        
        for index in indexes:
            try:
                collection.create_index(index)
                print(f"Created index: {index}")
            except Exception as e:
                print(f"Index creation failed for {index}: {e}")
        
        print("Database initialization completed")
        return True
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False

def get_database_stats():
    """Get database statistics"""
    try:
        connection = MongoDBConnection()
        db = connection.get_database()
        collection = connection.get_collection()
        
        if db is None or collection is None:
            return None
        
        stats = {
            'database_name': db.name,
            'collection_name': collection.name,
            'document_count': collection.count_documents({}),
            'indexes': list(collection.list_indexes()),
            'connection_status': connection.test_connection()
        }
        
        return stats
        
    except Exception as e:
        print(f"Failed to get database stats: {e}")
        return None

# Utility function for testing
def test_mongodb_setup():
    """Test complete MongoDB setup"""
    print("Testing MongoDB setup...")
    
    # Test connection
    connection = MongoDBConnection()
    if not connection.test_connection():
        print("  MongoDB connection failed")
        return False
    print("   MongoDB connection successful")
    
    # Initialize database
    if not initialize_database():
        print("  Database initialization failed")
        return False
    print("   Database initialization successful")
    
    # Get stats
    stats = get_database_stats()
    if stats:
        print("   Database stats retrieved:")
        print(f"   Database: {stats['database_name']}")
        print(f"   Collection: {stats['collection_name']}")
        print(f"   Documents: {stats['document_count']}")
        print(f"   Indexes: {len(stats['indexes'])}")
    else:
        print("  Failed to retrieve database stats")
        return False
    
    print("   MongoDB setup test completed successfully")
    return True

if __name__ == "__main__":
    test_mongodb_setup()
