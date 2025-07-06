"""
Data Display System
Polls MongoDB every 15 seconds and displays changes in the specified format
"""
import time
import os
from datetime import datetime, timedelta
from models.repository_data import RepositoryDataModel
from database.connection import MongoDBConnection
from dotenv import load_dotenv

load_dotenv()

class DataDisplaySystem:
    def __init__(self):
        self.repo_model = RepositoryDataModel()
        self.last_check_time = datetime.utcnow() - timedelta(seconds=15)  # Start with 15 seconds ago
        self.poll_interval = 15  # seconds
        self.running = False
        
    def format_display_data(self, data_list):
        """Format data according to the specified display format"""
        if not data_list:
            return "No new data to display"
        
        output_lines = []
        output_lines.append("=" * 60)
        output_lines.append(f"Repository Data Update - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        output_lines.append("=" * 60)
        
        for item in data_list:
            # Format according to the specification
            author = item.get('author', 'unknown')
            pushed_to = item.get('pushed_to', 'unknown')
            on_time = item.get('on', 'unknown')
            sample = item.get('sample', 'No description')
            
            # Parse the timestamp for better display
            try:
                if isinstance(on_time, str):
                    # Try to parse ISO format timestamp
                    if 'T' in on_time:
                        parsed_time = datetime.fromisoformat(on_time.replace('Z', '+00:00'))
                        formatted_time = parsed_time.strftime('%d %b %Y - %H:%M UTC')
                    else:
                        formatted_time = on_time
                else:
                    formatted_time = str(on_time)
            except:
                formatted_time = str(on_time)
            
            # Display format as specified in the requirements
            output_lines.append(f"Author: {author}")
            output_lines.append(f"Pushed to: {pushed_to}")
            output_lines.append(f"On: {formatted_time}")
            output_lines.append(f"Sample: {sample}")
            output_lines.append("-" * 40)
        
        output_lines.append(f"Total records: {len(data_list)}")
        output_lines.append("=" * 60)
        
        return "\n".join(output_lines)
    
    def get_new_data(self):
        """Get data that has been added since the last check"""
        try:
            new_data = self.repo_model.get_data_since(self.last_check_time)
            self.last_check_time = datetime.utcnow()
            return new_data
        except Exception as e:
            print(f"Error fetching new data: {e}")
            return []
    
    def display_recent_data(self, limit=10):
        """Display recent data for initial view"""
        try:
            recent_data = self.repo_model.get_recent_data(limit)
            if recent_data:
                print(self.format_display_data(recent_data))
            else:
                print("No data found in the database")
        except Exception as e:
            print(f"Error displaying recent data: {e}")
    
    def start_polling(self):
        """Start the polling loop"""
        self.running = True
        print(f"Starting data display system...")
        print(f"Polling interval: {self.poll_interval} seconds")
        print(f"MongoDB URI: {os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')}")
        print("-" * 60)
        
        # Display initial recent data
        print("Displaying recent data from database:")
        self.display_recent_data()
        
        print(f"\nStarting live polling (every {self.poll_interval} seconds)...")
        print("Press Ctrl+C to stop")
        print("-" * 60)
        
        try:
            while self.running:
                # Get new data since last check
                new_data = self.get_new_data()
                
                if new_data:
                    print(f"\n🔔 New data detected at {datetime.utcnow().strftime('%H:%M:%S')}")
                    print(self.format_display_data(new_data))
                else:
                    # Show a heartbeat message every 15 seconds
                    current_time = datetime.utcnow()
                    print(f"⏰ {current_time.strftime('%H:%M:%S')} - Monitoring for changes...")

                # Wait for next poll
                time.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping data display system...")
            self.stop_polling()
        except Exception as e:
            print(f"\n❌ Error in polling loop: {e}")
            self.stop_polling()
    
    def stop_polling(self):
        """Stop the polling loop"""
        self.running = False
        self.repo_model.close_connection()
        print("Data display system stopped")

def test_database_connection():
    """Test database connection before starting"""
    try:
        connection = MongoDBConnection()
        if connection.test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Main function to run the data display system"""
    print("GitHub Webhook Data Display System")
    print("=" * 50)
    
    # Test database connection first
    if not test_database_connection():
        print("Please ensure MongoDB is running and accessible")
        return
    
    # Initialize and start the display system
    display_system = DataDisplaySystem()
    
    try:
        display_system.start_polling()
    except Exception as e:
        print(f"Failed to start display system: {e}")

if __name__ == "__main__":
    main()
