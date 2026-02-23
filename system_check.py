#!/usr/bin/env python3
"""System checker tool - validates system requirements and tools."""

import os
from check_utils import run_command_check, print_summary_and_exit


def check_git_installed():
    """Check if git is installed."""
    return run_command_check(['git', '--version'], 'Git')


def check_python_installed():
    """Check if python is installed."""
    return run_command_check(['python3', '--version'], 'Python')


def check_node_installed():
    """Check if node is installed."""
    return run_command_check(['node', '--version'], 'Node')


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
    
    print_summary_and_exit(results)


if __name__ == "__main__":
    main()
