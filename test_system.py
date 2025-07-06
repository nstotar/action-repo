"""
System Testing Script
Tests the complete GitHub webhook MongoDB integration workflow
"""
import requests
import json
import time
import os
from datetime import datetime
from models.repository_data import RepositoryDataModel
from database.connection import MongoDBConnection, test_mongodb_setup

class SystemTester:
    def __init__(self):
        self.webhook_url = "http://localhost:5000"
        self.repo_model = RepositoryDataModel()
        self.test_results = []
    
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def test_database_connection(self):
        """Test MongoDB connection"""
        try:
            connection = MongoDBConnection()
            success = connection.test_connection()
            self.log_test("Database Connection", success, 
                         "Connected to MongoDB" if success else "Failed to connect to MongoDB")
            return success
        except Exception as e:
            self.log_test("Database Connection", False, str(e))
            return False
    
    def test_webhook_receiver_health(self):
        """Test webhook receiver health endpoint"""
        try:
            response = requests.get(f"{self.webhook_url}/health", timeout=5)
            success = response.status_code == 200
            self.log_test("Webhook Receiver Health", success, 
                         f"Status: {response.status_code}" if success else "Health check failed")
            return success
        except Exception as e:
            self.log_test("Webhook Receiver Health", False, str(e))
            return False
    
    def create_test_push_payload(self):
        """Create a test push webhook payload"""
        return {
            "ref": "refs/heads/main",
            "repository": {
                "name": "test-repo",
                "full_name": "testuser/test-repo"
            },
            "pusher": {
                "name": "test_user"
            },
            "head_commit": {
                "id": "abc123def456",
                "message": "Test commit for system validation",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "author": {
                    "name": "test_user",
                    "email": "test@example.com"
                }
            }
        }
    
    def create_test_pr_payload(self):
        """Create a test pull request webhook payload"""
        return {
            "action": "opened",
            "repository": {
                "name": "test-repo",
                "full_name": "testuser/test-repo"
            },
            "pull_request": {
                "number": 42,
                "title": "Test Pull Request for System Validation",
                "user": {
                    "login": "test_user"
                },
                "base": {
                    "ref": "main"
                },
                "head": {
                    "ref": "feature-test"
                },
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z"
            }
        }
    
    def test_push_webhook(self):
        """Test push webhook processing"""
        try:
            payload = self.create_test_push_payload()
            headers = {
                'Content-Type': 'application/json',
                'X-GitHub-Event': 'push',
                'X-GitHub-Delivery': 'test-push-' + str(int(time.time()))
            }
            
            response = requests.post(f"{self.webhook_url}/webhook", 
                                   json=payload, headers=headers, timeout=10)
            
            success = response.status_code == 200
            message = f"Status: {response.status_code}, Response: {response.text[:100]}"
            self.log_test("Push Webhook Processing", success, message)
            return success
        except Exception as e:
            self.log_test("Push Webhook Processing", False, str(e))
            return False
    
    def test_pull_request_webhook(self):
        """Test pull request webhook processing"""
        try:
            payload = self.create_test_pr_payload()
            headers = {
                'Content-Type': 'application/json',
                'X-GitHub-Event': 'pull_request',
                'X-GitHub-Delivery': 'test-pr-' + str(int(time.time()))
            }
            
            response = requests.post(f"{self.webhook_url}/webhook", 
                                   json=payload, headers=headers, timeout=10)
            
            success = response.status_code == 200
            message = f"Status: {response.status_code}, Response: {response.text[:100]}"
            self.log_test("Pull Request Webhook Processing", success, message)
            return success
        except Exception as e:
            self.log_test("Pull Request Webhook Processing", False, str(e))
            return False
    
    def test_data_storage(self):
        """Test data storage in MongoDB"""
        try:
            # Get initial count
            initial_data = self.repo_model.get_recent_data(1)
            initial_count = len(initial_data)
            
            # Send a test webhook
            self.test_push_webhook()
            
            # Wait a moment for processing
            time.sleep(2)
            
            # Check if data was stored
            new_data = self.repo_model.get_recent_data(5)
            new_count = len(new_data)
            
            success = new_count > initial_count
            message = f"Data count increased from {initial_count} to {new_count}"
            self.log_test("Data Storage", success, message)
            
            if success and new_data:
                # Validate data structure
                latest_record = new_data[0]
                required_fields = ['author', 'pushed_to', 'on', 'sample']
                has_all_fields = all(field in latest_record for field in required_fields)
                self.log_test("Data Structure Validation", has_all_fields,
                             f"Latest record has all required fields: {list(latest_record.keys())}")
            
            return success
        except Exception as e:
            self.log_test("Data Storage", False, str(e))
            return False
    
    def test_data_retrieval(self):
        """Test data retrieval from webhook receiver"""
        try:
            response = requests.get(f"{self.webhook_url}/recent?limit=5", timeout=5)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = data.get('count', 0)
                message = f"Retrieved {count} records successfully"
            else:
                message = f"Failed with status {response.status_code}"
            
            self.log_test("Data Retrieval API", success, message)
            return success
        except Exception as e:
            self.log_test("Data Retrieval API", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all system tests"""
        print("GitHub Webhook MongoDB Integration - System Tests")
        print("=" * 60)
        
        # Test sequence
        tests = [
            ("Database Setup", test_mongodb_setup),
            ("Database Connection", self.test_database_connection),
            ("Webhook Receiver Health", self.test_webhook_receiver_health),
            ("Push Webhook", self.test_push_webhook),
            ("Pull Request Webhook", self.test_pull_request_webhook),
            ("Data Storage", self.test_data_storage),
            ("Data Retrieval", self.test_data_retrieval)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {e}")
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! System is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please check the system configuration.")
        
        return passed == total
    
    def cleanup(self):
        """Cleanup test resources"""
        try:
            self.repo_model.close_connection()
        except:
            pass

def main():
    """Main testing function"""
    tester = SystemTester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user")
        return 1
    except Exception as e:
        print(f"\nTesting failed with error: {e}")
        return 1
    finally:
        tester.cleanup()

if __name__ == "__main__":
    exit(main())
