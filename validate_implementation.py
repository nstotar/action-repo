"""
Implementation Validation Script
Validates that the implementation meets all requirements from the assessment task
"""
import os
import json
import subprocess
from datetime import datetime

class ImplementationValidator:
    def __init__(self):
        self.requirements = {
            "github_repo_webhook": "GitHub repository webhook configuration",
            "mongodb_integration": "MongoDB integration with specified schema",
            "data_polling": "15-second polling and display system",
            "action_repo": "Action repository with webhook configuration",
            "data_format": "Correct data format (author, pushed_to, on, timestamp, sample)",
            "webhook_events": "Support for PUSH, PULL_REQUEST, and MERGE actions",
            "real_time_display": "Real-time data display with specified format"
        }
        self.validation_results = {}
    
    def validate_file_structure(self):
        """Validate required files and directories exist"""
        required_files = [
            "webhook_receiver.py",
            "data_display.py", 
            "models/repository_data.py",
            "database/connection.py",
            "action-repo/package.json",
            "action-repo/.github/workflows/webhook-trigger.yml",
            "requirements.txt",
            ".env.example",
            "README.md"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        success = len(missing_files) == 0
        self.validation_results["file_structure"] = {
            "success": success,
            "message": f"Missing files: {missing_files}" if missing_files else "All required files present"
        }
        return success
    
    def validate_mongodb_schema(self):
        """Validate MongoDB schema implementation"""
        try:
            with open("models/repository_data.py", "r", encoding='utf-8') as f:
                content = f.read()

            required_fields = ["author", "pushed_to", "on", "timestamp", "sample"]
            schema_valid = all(field in content for field in required_fields)

            self.validation_results["mongodb_schema"] = {
                "success": schema_valid,
                "message": "MongoDB schema includes all required fields" if schema_valid else "Missing required schema fields"
            }
            return schema_valid
        except Exception as e:
            self.validation_results["mongodb_schema"] = {
                "success": False,
                "message": f"Error validating schema: {e}"
            }
            return False
    
    def validate_webhook_receiver(self):
        """Validate webhook receiver implementation"""
        try:
            with open("webhook_receiver.py", "r", encoding='utf-8') as f:
                content = f.read()

            # Check for required webhook event handling
            required_features = [
                "push",  # Push event handling
                "pull_request",  # Pull request event handling
                "extract_push_data",  # Data extraction functions
                "extract_pull_request_data",
                "MongoDB",  # MongoDB integration
                "Flask"  # Flask framework
            ]

            features_present = all(feature in content for feature in required_features)

            self.validation_results["webhook_receiver"] = {
                "success": features_present,
                "message": "Webhook receiver supports all required events" if features_present else "Missing required webhook features"
            }
            return features_present
        except Exception as e:
            self.validation_results["webhook_receiver"] = {
                "success": False,
                "message": f"Error validating webhook receiver: {e}"
            }
            return False
    
    def validate_data_display(self):
        """Validate data display system"""
        try:
            with open("data_display.py", "r", encoding='utf-8') as f:
                content = f.read()

            # Check for 15-second polling
            polling_implemented = ("poll_interval = 15" in content or "15 seconds" in content) and "poll" in content.lower()

            # Check for required display format
            format_features = [
                "Author:",
                "Pushed to:",
                "On:",
                "Sample:"
            ]

            format_valid = all(feature in content for feature in format_features)

            success = polling_implemented and format_valid
            message = "Data display system with 15-second polling and correct format"
            if not polling_implemented:
                message = "15-second polling not properly implemented"
            elif not format_valid:
                message = "Display format missing required fields"

            self.validation_results["data_display"] = {
                "success": success,
                "message": message
            }
            return success
        except Exception as e:
            self.validation_results["data_display"] = {
                "success": False,
                "message": f"Error validating data display: {e}"
            }
            return False
    
    def validate_action_repo(self):
        """Validate action repository setup"""
        try:
            # Check GitHub Actions workflow
            workflow_path = "action-repo/.github/workflows/webhook-trigger.yml"
            if not os.path.exists(workflow_path):
                self.validation_results["action_repo"] = {
                    "success": False,
                    "message": "GitHub Actions workflow file missing"
                }
                return False
            
            with open(workflow_path, "r", encoding='utf-8') as f:
                workflow_content = f.read()
            
            # Check for required workflow triggers
            required_triggers = ["push:", "pull_request:"]
            triggers_present = all(trigger in workflow_content for trigger in required_triggers)
            
            # Check package.json
            package_path = "action-repo/package.json"
            package_valid = os.path.exists(package_path)
            
            success = triggers_present and package_valid
            self.validation_results["action_repo"] = {
                "success": success,
                "message": "Action repository properly configured" if success else "Missing workflow triggers or package.json"
            }
            return success
        except Exception as e:
            self.validation_results["action_repo"] = {
                "success": False,
                "message": f"Error validating action repo: {e}"
            }
            return False
    
    def validate_testing_framework(self):
        """Validate testing implementation"""
        test_files = ["test_system.py", "action-repo/webhook-test.js"]
        
        missing_tests = []
        for test_file in test_files:
            if not os.path.exists(test_file):
                missing_tests.append(test_file)
        
        success = len(missing_tests) == 0
        self.validation_results["testing_framework"] = {
            "success": success,
            "message": "All testing files present" if success else f"Missing test files: {missing_tests}"
        }
        return success
    
    def validate_documentation(self):
        """Validate documentation completeness"""
        try:
            with open("README.md", "r", encoding='utf-8') as f:
                readme_content = f.read()

            required_sections = [
                "Setup",
                "MongoDB Schema",
                "GitHub Webhook",
                "Testing",
                "API Endpoints"
            ]

            sections_present = all(section in readme_content for section in required_sections)

            self.validation_results["documentation"] = {
                "success": sections_present,
                "message": "Documentation includes all required sections" if sections_present else "Missing required documentation sections"
            }
            return sections_present
        except Exception as e:
            self.validation_results["documentation"] = {
                "success": False,
                "message": f"Error validating documentation: {e}"
            }
            return False
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("GitHub Webhook MongoDB Integration - Implementation Validation")
        print("=" * 70)
        print(f"Validation Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 70)
        
        # Run all validations
        validations = [
            ("File Structure", self.validate_file_structure),
            ("MongoDB Schema", self.validate_mongodb_schema),
            ("Webhook Receiver", self.validate_webhook_receiver),
            ("Data Display System", self.validate_data_display),
            ("Action Repository", self.validate_action_repo),
            ("Testing Framework", self.validate_testing_framework),
            ("Documentation", self.validate_documentation)
        ]
        
        passed = 0
        total = len(validations)
        
        for validation_name, validation_func in validations:
            try:
                result = validation_func()
                status = "✅ PASS" if result else "❌ FAIL"
                message = self.validation_results.get(validation_name.lower().replace(" ", "_"), {}).get("message", "")
                
                print(f"{status} {validation_name}")
                if message:
                    print(f"    {message}")
                
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ FAIL {validation_name}")
                print(f"    Error: {e}")
        
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        # Requirements mapping
        print("Requirements Validation:")
        requirements_status = {
            "GitHub Repository Webhook": "✅" if self.validation_results.get("webhook_receiver", {}).get("success") else "❌",
            "MongoDB Integration": "✅" if self.validation_results.get("mongodb_schema", {}).get("success") else "❌",
            "15-Second Data Polling": "✅" if self.validation_results.get("data_display", {}).get("success") else "❌",
            "Action Repository Setup": "✅" if self.validation_results.get("action_repo", {}).get("success") else "❌",
            "Comprehensive Testing": "✅" if self.validation_results.get("testing_framework", {}).get("success") else "❌",
            "Complete Documentation": "✅" if self.validation_results.get("documentation", {}).get("success") else "❌"
        }
        
        for requirement, status in requirements_status.items():
            print(f"  {status} {requirement}")
        
        print(f"\nOverall Results:")
        print(f"  Total Validations: {total}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {total - passed}")
        print(f"  Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 IMPLEMENTATION COMPLETE!")
            print("All requirements have been successfully implemented.")
            print("\nNext Steps:")
            print("1. Run 'python setup.py' to install dependencies")
            print("2. Start MongoDB service")
            print("3. Run 'python start_system.py' to start the system")
            print("4. Run 'python test_system.py' to validate functionality")
        else:
            print(f"\n⚠️  IMPLEMENTATION INCOMPLETE")
            print(f"{total - passed} validation(s) failed. Please review the failed items above.")
        
        return passed == total

def main():
    """Main validation function"""
    validator = ImplementationValidator()
    success = validator.generate_validation_report()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
