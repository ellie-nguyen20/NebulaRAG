#!/usr/bin/env python3
"""
Comprehensive test suite for NebulaRAG
Runs all 15 test scenarios automatically
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Load .env file manually
def load_env_file():
    """Load .env file manually"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load environment variables
load_env_file()

class RAGTestSuite:
    def __init__(self):
        self.results = []
        self.docs_dir = Path("docs")
        self.test_dir = Path("test_docs")
        
    def run_command(self, cmd, description):
        """Run a command and record results"""
        print(f"\n{'='*60}")
        print(f"TEST: {description}")
        print(f"COMMAND: {cmd}")
        print(f"{'='*60}")
        
        start_time = time.time()
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            duration = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ PASSED ({duration:.2f}s)")
                print("OUTPUT:")
                print(result.stdout)
                self.results.append(("PASS", description, duration))
            else:
                print(f"❌ FAILED ({duration:.2f}s)")
                print("ERROR:")
                print(result.stderr)
                self.results.append(("FAIL", description, duration))
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT (120s)")
            self.results.append(("TIMEOUT", description, 120))
        except Exception as e:
            print(f"💥 ERROR: {e}")
            self.results.append(("ERROR", description, 0))
    
    def setup_test_environment(self):
        """Setup test environment"""
        print("Setting up test environment...")
        
        # Create test directory
        self.test_dir.mkdir(exist_ok=True)
        
        # Create empty docs directory
        empty_docs = Path("empty_docs")
        empty_docs.mkdir(exist_ok=True)
        
        # Create large document
        with open(self.docs_dir / "large_doc.txt", "w") as f:
            for i in range(100):
                f.write(f"This is paragraph {i}. It contains information about topic {i%10}.\n")
        
        # Create additional test files
        with open(self.docs_dir / "test.txt", "w") as f:
            f.write("This is a text file about machine learning and artificial intelligence.")
        
        with open(self.docs_dir / "test.md", "w") as f:
            f.write("# Markdown File\n\nThis is a markdown file about AI and deep learning.")
    
    def run_basic_tests(self):
        """Run basic functionality tests"""
        print("\n🔍 RUNNING BASIC TESTS...")
        
        # Test 1: API Connection
        self.run_command("cd scripts && python3 test_nebula.py", "API Connection Test")
        
        # Test 2: Module Import
        self.run_command("python3 quick_test.py", "Module Import Test")
        
        # Test 3: Basic Question
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is this document about?"', "Basic Question Test")
        
        # Test 4: Out-of-scope Question
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is quantum computing?"', "Out-of-scope Question Test")
    
    def run_parameter_tests(self):
        """Run parameter variation tests"""
        print("\n⚙️ RUNNING PARAMETER TESTS...")
        
        # Test 5: Small chunks
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is the main topic?" --chunk-size 200 --chunk-overlap 50', "Small Chunks Test")
        
        # Test 6: Large chunks
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is the main topic?" --chunk-size 1500 --chunk-overlap 200', "Large Chunks Test")
        
        # Test 7: Low top-k
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is the main topic?" --top-k 3 --rerank-k 2', "Low Top-K Test")
        
        # Test 8: High top-k
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is the main topic?" --top-k 20 --rerank-k 10', "High Top-K Test")
    
    def run_question_type_tests(self):
        """Run different question type tests"""
        print("\n❓ RUNNING QUESTION TYPE TESTS...")
        
        # Test 9: Specific question
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What are the specific steps in the pipeline flow?"', "Specific Question Test")
        
        # Test 10: Comparison question
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "Compare the different approaches mentioned in the documents"', "Comparison Question Test")
        
        # Test 11: Open question
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What can you tell me about this topic?"', "Open Question Test")
        
        # Test 12: Negative question
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What is NOT mentioned in the documents?"', "Negative Question Test")
    
    def run_document_tests(self):
        """Run document handling tests"""
        print("\n📄 RUNNING DOCUMENT TESTS...")
        
        # Test 13: Empty documents
        self.run_command('python3 -m nebularag.cli.main --docs empty_docs --question "What is this about?"', "Empty Documents Test")
        
        # Test 14: Large document
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What are the main topics in the large document?"', "Large Document Test")
        
        # Test 15: Multiple file types
        self.run_command('python3 -m nebularag.cli.main --docs docs --question "What types of files are processed?"', "Multiple File Types Test")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        passed = sum(1 for status, _, _ in self.results if status == "PASS")
        failed = sum(1 for status, _, _ in self.results if status == "FAIL")
        timeout = sum(1 for status, _, _ in self.results if status == "TIMEOUT")
        error = sum(1 for status, _, _ in self.results if status == "ERROR")
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏰ Timeout: {timeout}")
        print(f"💥 Error: {error}")
        print(f"Success Rate: {passed/total*100:.1f}%")
        
        print("\nDetailed Results:")
        for i, (status, description, duration) in enumerate(self.results, 1):
            status_icon = {"PASS": "✅", "FAIL": "❌", "TIMEOUT": "⏰", "ERROR": "💥"}[status]
            print(f"{i:2d}. {status_icon} {description} ({duration:.2f}s)")
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("🧪 NEBULARAG COMPREHENSIVE TEST SUITE")
        print("="*80)
        
        # Check if API key is set
        if not os.environ.get("NEBULABLOCK_API_KEY"):
            print("❌ ERROR: NEBULABLOCK_API_KEY environment variable is not set")
            print("Please set your API key in .env file or environment")
            return False
        
        try:
            self.setup_test_environment()
            self.run_basic_tests()
            self.run_parameter_tests()
            self.run_question_type_tests()
            self.run_document_tests()
            self.print_summary()
            return True
        except KeyboardInterrupt:
            print("\n\n⚠️ Tests interrupted by user")
            return False
        except Exception as e:
            print(f"\n\n💥 Unexpected error: {e}")
            return False

def main():
    """Main function"""
    test_suite = RAGTestSuite()
    success = test_suite.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
