#!/usr/bin/env python3
"""Simple tests to verify the refactored checker utilities."""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_utils import run_command_check, check_http_request


def test_run_command_check():
    """Test the run_command_check utility function."""
    print("Testing run_command_check...")
    
    # Test with a command that should succeed
    result = run_command_check(['echo', 'test'], 'Echo')
    assert result is True, "Echo command should succeed"
    print("✓ Test passed: run_command_check with successful command")
    
    # Test with a command that should fail (non-existent command)
    result = run_command_check(['nonexistent_command_xyz'], 'NonExistent')
    assert result is False, "Non-existent command should fail"
    print("✓ Test passed: run_command_check with failing command")


def test_http_request():
    """Test the check_http_request utility function."""
    print("\nTesting check_http_request...")
    
    # Test with a valid URL (Google)
    result = check_http_request('https://www.google.com', protocol='HTTPS', verify=True)
    if result:
        print("✓ Test passed: check_http_request with valid URL")
    else:
        print("⚠ Warning: Could not connect to Google (network issue?)")
    
    # Test with an invalid URL
    result = check_http_request('http://definitely-not-a-real-domain-12345.com', protocol='HTTP', verify=False)
    assert result is False, "Invalid domain should fail"
    print("✓ Test passed: check_http_request with invalid URL")


def main():
    """Run all tests."""
    print("=== Running Tests for Refactored Code ===\n")
    
    try:
        test_run_command_check()
        test_http_request()
        
        print("\n=== All Tests Passed ===")
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
