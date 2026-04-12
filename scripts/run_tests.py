import os
import sys
import unittest
from pathlib import Path

def main():
    root_dir = Path(__file__).parent.parent
    tests_dir = root_dir / "tests"
    
    if not tests_dir.exists():
        print(f"Error: tests directory not found at {tests_dir}")
        sys.exit(1)
        
    print(f"Running Iconora Studio Backend Tests...")
    print(f"Root: {root_dir}")
    
    # Ensure root is in PYTHONPATH
    sys.path.insert(0, str(root_dir))
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(tests_dir), pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    main()
