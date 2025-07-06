"""
Setup and Installation Script
Installs dependencies and sets up the GitHub webhook MongoDB integration system
"""
import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f" {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f" {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f" {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(" Python 3.7 or higher is required")
        return False
    print(f" Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_mongodb():
    """Check if MongoDB is available"""
    try:
        result = subprocess.run("mongod --version", shell=True, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(" MongoDB is installed")
            return True
    except:
        pass
    
    print("  MongoDB not detected. Please install MongoDB:")
    print("   - Windows: Download from https://www.mongodb.com/try/download/community")
    print("   - macOS: brew install mongodb-community")
    print("   - Ubuntu: sudo apt-get install mongodb")
    return False

def install_python_dependencies():
    """Install Python dependencies"""
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing Python dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def install_node_dependencies():
    """Install Node.js dependencies for action-repo"""
    if not os.path.exists("action-repo"):
        print(" action-repo directory not found, skipping Node.js setup")
        return True
    
    original_dir = os.getcwd()
    try:
        os.chdir("action-repo")
        success = run_command("npm install", "Installing Node.js dependencies")
        return success
    finally:
        os.chdir(original_dir)

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data", "temp"]
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"    Created directory: {directory}")
        except Exception as e:
            print(f"    Failed to create directory {directory}: {e}")
            return False
    return True

def setup_environment():
    """Set up environment configuration"""
    if not os.path.exists(".env"):
        print("     .env file not found, using .env.example")
        try:
            with open(".env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print("    Created .env file from .env.example")
        except Exception as e:
            print(f"    Failed to create .env file: {e}")
            return False
    else:
        print("    .env file already exists")
    return True

def test_installation():
    """Test the installation"""
    print("\n    Testing installation...")
    
    # Test Python imports
    try:
        from models.repository_data import RepositoryDataModel
        from database.connection import MongoDBConnection
        print("    Python modules import successfully")
    except ImportError as e:
        print(f"    Python module import failed: {e}")
        return False
    
    # Test MongoDB connection (if available)
    try:
        from database.connection import test_mongodb_setup
        if test_mongodb_setup():
            print("    MongoDB connection test passed")
        else:
            print("     MongoDB connection test failed (MongoDB may not be running)")
    except Exception as e:
        print(f"     MongoDB test error: {e}")
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("    SETUP COMPLETED!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start MongoDB (if not already running):")
    print("   mongod")
    print("\n2. Start the webhook receiver:")
    print("   python webhook_receiver.py")
    print("\n3. Start the data display system (in another terminal):")
    print("   python data_display.py")
    print("\n4. Or start both systems together:")
    print("   python start_system.py")
    print("\n5. Test the system:")
    print("   python test_system.py")
    print("\n6. Test webhooks from action-repo:")
    print("   cd action-repo")
    print("   npm run webhook-test")
    print("\n    Webhook endpoint will be available at:")
    print("   http://localhost:5000/webhook")
    print("\n    Health check endpoint:")
    print("   http://localhost:5000/health")
    print("\n" + "=" * 60)

def main():
    """Main setup function"""
    print("GitHub Webhook MongoDB Integration - Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return 1
    
    check_mongodb()  # Warning only, not blocking
    
    # Setup steps
    setup_steps = [
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment),
        ("Installing Python dependencies", install_python_dependencies),
        ("Installing Node.js dependencies", install_node_dependencies),
        ("Testing installation", test_installation)
    ]
    
    for step_name, step_func in setup_steps:
        print(f"\n    {step_name}...")
        if not step_func():
            print(f"    Setup failed at step: {step_name}")
            return 1
    
    print_next_steps()
    return 0

if __name__ == "__main__":
    exit(main())
