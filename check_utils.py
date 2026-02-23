#!/usr/bin/env python3
"""Common utility functions for various checker tools."""

import sys
import subprocess
import requests


def run_command_check(command, tool_name, description=None):
    """
    Generic subprocess command checker.
    
    Args:
        command: List of command arguments (e.g., ['git', '--version'])
        tool_name: Human-readable name of the tool
        description: Optional description of what is being checked
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    desc = description or f"if {tool_name} is installed"
    print(f"Checking {desc}...")
    try:
        result = subprocess.run(command, 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ {tool_name} is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {tool_name} check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ {tool_name} is not installed: {e}")
        return False


def check_http_request(url, protocol="HTTP", verify=False):
    """
    Generic HTTP(S) request checker.
    
    Args:
        url: The URL to check
        protocol: Protocol name for display purposes (HTTP/HTTPS)
        verify: Whether to verify SSL certificates
        
    Returns:
        bool: True if request succeeded with 200, False otherwise
        
    Security Note:
        When verify=False, SSL certificate validation is disabled. This should
        only be used for testing purposes or when checking HTTP (not HTTPS) URLs.
        For production HTTPS checks, always use verify=True to prevent MITM attacks.
    """
    if not verify and protocol.upper() == "HTTPS":
        print(f"⚠ Warning: SSL certificate verification is disabled for {url}")
    
    print(f"Checking {protocol} connectivity for {url}...")
    try:
        response = requests.get(url, timeout=5, verify=verify)
        if response.status_code == 200:
            print(f"✓ {url} is accessible via {protocol} (Status: {response.status_code})")
            return True
        else:
            print(f"✗ {url} returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Error connecting to {url} via {protocol}: {e}")
        return False


def print_summary_and_exit(results, title="Summary"):
    """
    Print standardized check summary and exit with appropriate code.
    
    Args:
        results: List of boolean check results
        title: Title for the summary section
        
    Exits with code 0 if all checks passed, 1 otherwise
    """
    print(f"\n=== {title} ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} checks")
    
    sys.exit(0 if passed == total else 1)
