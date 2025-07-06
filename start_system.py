"""
System Startup Script
Starts both the webhook receiver and data display system
"""
import subprocess
import sys
import os
import time
import signal
from multiprocessing import Process
from database.connection import test_mongodb_setup

def start_webhook_receiver():
    """Start the webhook receiver"""
    try:
        print("Starting webhook receiver...")
        os.system("python webhook_receiver.py")
    except Exception as e:
        print(f"Error starting webhook receiver: {e}")

def start_data_display():
    """Start the data display system"""
    try:
        print("Starting data display system...")
        os.system("python data_display.py")
    except Exception as e:
        print(f"Error starting data display system: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\nShutting down system...")
    sys.exit(0)

def main():
    """Main function to start the complete system"""
    print("GitHub Webhook MongoDB Integration System")
    print("=" * 50)
    
    # Test MongoDB setup
    print("Testing MongoDB setup...")
    if not test_mongodb_setup():
        print("❌ MongoDB setup failed. Please check your MongoDB installation and configuration.")
        return
    
    print("✅ MongoDB setup successful")
    print("-" * 50)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start webhook receiver in a separate process
        webhook_process = Process(target=start_webhook_receiver)
        webhook_process.start()
        
        # Give webhook receiver time to start
        time.sleep(2)
        
        # Start data display in a separate process
        display_process = Process(target=start_data_display)
        display_process.start()
        
        print("✅ Both systems started successfully")
        print("📡 Webhook receiver: http://localhost:5000/webhook")
        print("📊 Data display: Running with 15-second polling")
        print("\nPress Ctrl+C to stop both systems")
        
        # Wait for processes
        webhook_process.join()
        display_process.join()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping all processes...")
        if 'webhook_process' in locals():
            webhook_process.terminate()
        if 'display_process' in locals():
            display_process.terminate()
    except Exception as e:
        print(f"❌ Error running system: {e}")

if __name__ == "__main__":
    main()
