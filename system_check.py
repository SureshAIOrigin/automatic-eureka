#!/usr/bin/env python3
"""System checker tool - validates system requirements and tools."""

import sys
import subprocess
import os
import shutil


def check_git_installed():
    """Check if git is installed."""
    print("Checking if git is installed...")
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ Git is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Git check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ Git is not installed: {e}")
        return False


def check_python_installed():
    """Check if python is installed."""
    print("Checking if python is installed...")
    try:
        result = subprocess.run(['python3', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ Python is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Python check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ Python is not installed: {e}")
        return False


def check_node_installed():
    """Check if node is installed."""
    print("Checking if node is installed...")
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ Node is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Node check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ Node is not installed: {e}")
        return False


def check_disk_space():
    """Check if sufficient disk space is available."""
    print("Checking disk space...")
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        print(f"✓ Free disk space: {free_gb:.2f} GB")
        if free_gb > 1:
            return True
        else:
            print(f"✗ Insufficient disk space (less than 1 GB)")
            return False
    except Exception as e:
        print(f"✗ Error checking disk space: {e}")
        return False


def check_write_permissions():
    """Check if we have write permissions in current directory."""
    print("Checking write permissions...")
    try:
        test_file = '.test_write_permissions'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print(f"✓ Write permissions verified")
        return True
    except Exception as e:
        print(f"✗ No write permissions: {e}")
        return False


def main():
    """Main function to run system checks."""
    print("\n=== System Checker ===\n")
    
    results = []
    results.append(check_git_installed())
    results.append(check_python_installed())
    results.append(check_node_installed())
    results.append(check_disk_space())
    results.append(check_write_permissions())
    
    print(f"\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} checks")
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
