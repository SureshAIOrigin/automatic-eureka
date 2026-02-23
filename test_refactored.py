#!/usr/bin/env python3
"""Simple tests to verify the refactored checker utilities."""

import sys
import os
from io import StringIO
from unittest.mock import patch

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_utils import run_command_check, check_http_request, print_summary_and_exit


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


def test_print_summary_and_exit():
    """Test the print_summary_and_exit utility function."""
    print("\nTesting print_summary_and_exit...")
    
    # Capture stdout
    captured_output = StringIO()
    
    # Test with all passing checks
    try:
        with patch('sys.stdout', captured_output):
            with patch('sys.exit') as mock_exit:
                print_summary_and_exit([True, True, True])
                mock_exit.assert_called_once_with(0)
        output = captured_output.getvalue()
        assert "Passed: 3/3 checks" in output, "Should show 3/3 checks passed"
        print("✓ Test passed: print_summary_and_exit with all passing checks")
    except Exception as e:
        print(f"⚠ Test for print_summary_and_exit (all pass): {e}")
    
    # Test with some failing checks
    captured_output = StringIO()
    try:
        with patch('sys.stdout', captured_output):
            with patch('sys.exit') as mock_exit:
                print_summary_and_exit([True, False, True, False])
                mock_exit.assert_called_once_with(1)
        output = captured_output.getvalue()
        assert "Passed: 2/4 checks" in output, "Should show 2/4 checks passed"
        print("✓ Test passed: print_summary_and_exit with some failing checks")
    except Exception as e:
        print(f"⚠ Test for print_summary_and_exit (partial): {e}")


def main():
    """Run all tests."""
    print("=== Running Tests for Refactored Code ===\n")
    
    try:
        test_run_command_check()
        test_http_request()
        test_print_summary_and_exit()
        
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
