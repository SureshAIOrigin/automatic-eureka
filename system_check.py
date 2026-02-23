#!/usr/bin/env python3
"""
System Check Script for automatic-eureka repository
Performs comprehensive system validation and health checks
"""

import os
import sys
import subprocess
import platform
from datetime import datetime


def print_header(text):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def print_check(check_name, check_passed, details=""):
    """Print a check result"""
    status_symbol = "✓" if check_passed else "✗"
    print(f"{status_symbol} {check_name}: {'PASS' if check_passed else 'FAIL'}")
    if details:
        print(f"  └─ {details}")


def check_python_version():
    """Check Python version"""
    print_header("Python Environment")
    version_info = sys.version_info
    print_check(
        "Python Version",
        True,
        f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    )
    return True


def check_git_repository():
    """Check Git repository status"""
    print_header("Git Repository Status")
    
    checks_passed_count = 0
    total_checks_count = 0
    
    # Check if git is available
    total_checks_count += 1
    try:
        command_result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        git_version = command_result.stdout.strip()
        print_check("Git Available", True, git_version)
        checks_passed_count += 1
    except (subprocess.SubprocessError, FileNotFoundError):
        print_check("Git Available", False, "Git not found")
        return False
    
    # Check if current directory is a git repository
    total_checks_count += 1
    try:
        command_result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if command_result.returncode == 0:
            print_check("Git Repository", True, ".git directory found")
            checks_passed_count += 1
        else:
            print_check("Git Repository", False, "Not a git repository")
    except subprocess.SubprocessError:
        print_check("Git Repository", False, "Git command failed")
    
    # Check current branch
    total_checks_count += 1
    try:
        command_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if command_result.returncode == 0:
            branch_name = command_result.stdout.strip()
            print_check("Current Branch", True, branch_name)
            checks_passed_count += 1
        else:
            print_check("Current Branch", False)
    except subprocess.SubprocessError:
        print_check("Current Branch", False, "Git command failed")
    
    # Check for uncommitted changes
    total_checks_count += 1
    try:
        command_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if command_result.returncode == 0:
            uncommitted_changes = command_result.stdout.strip()
            has_uncommitted_changes = len(uncommitted_changes) > 0
            print_check(
                "Working Directory",
                True,
                "Clean" if not has_uncommitted_changes else f"{len(uncommitted_changes.splitlines())} uncommitted changes"
            )
            checks_passed_count += 1
    except subprocess.SubprocessError:
        print_check("Working Directory", False, "Git command failed")
    
    return checks_passed_count == total_checks_count


def check_file_system():
    """Check file system and repository structure"""
    print_header("File System Checks")
    
    checks_passed_count = 0
    total_checks_count = 0
    
    # Check if README exists
    total_checks_count += 1
    readme_exists = os.path.isfile("README.md")
    print_check("README.md", readme_exists)
    if readme_exists:
        checks_passed_count += 1
        # Check README size
        file_size = os.path.getsize("README.md")
        print(f"  └─ Size: {file_size} bytes")
    
    # Check directory permissions
    total_checks_count += 1
    try:
        can_read = os.access(".", os.R_OK)
        can_write = os.access(".", os.W_OK)
        can_execute = os.access(".", os.X_OK)
        
        permissions_valid = can_read and can_write and can_execute
        print_check(
            "Directory Permissions",
            permissions_valid,
            f"Read: {can_read}, Write: {can_write}, Execute: {can_execute}"
        )
        if permissions_valid:
            checks_passed_count += 1
    except Exception as error:
        print_check("Directory Permissions", False, str(error))
    
    # Check disk space
    total_checks_count += 1
    try:
        import shutil
        disk_usage = shutil.disk_usage(".")
        free_space_gb = disk_usage.free / (1024 ** 3)
        total_space_gb = disk_usage.total / (1024 ** 3)
        percent_free = (disk_usage.free / disk_usage.total) * 100
        
        has_sufficient_disk_space = percent_free > 10  # At least 10% free
        print_check(
            "Disk Space",
            has_sufficient_disk_space,
            f"{free_space_gb:.2f} GB free of {total_space_gb:.2f} GB ({percent_free:.1f}%)"
        )
        if has_sufficient_disk_space:
            checks_passed_count += 1
    except Exception as error:
        print_check("Disk Space", False, str(error))
    
    return checks_passed_count == total_checks_count


def check_system_info():
    """Display system information"""
    print_header("System Information")
    
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"Hostname: {platform.node()}")
    print(f"Current Directory: {os.getcwd()}")
    print(f"User: {os.environ.get('USER', 'unknown')}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    return True


def check_common_tools():
    """Check for common development tools"""
    print_header("Development Tools")
    
    tools_to_check = [
        ("git", ["git", "--version"]),
        ("python3", ["python3", "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("docker", ["docker", "--version"]),
    ]
    
    available_tools_count = 0
    
    for tool_name, version_command in tools_to_check:
        try:
            command_result = subprocess.run(
                version_command,
                capture_output=True,
                text=True,
                timeout=5
            )
            if command_result.returncode == 0:
                version_string = command_result.stdout.strip().split("\n")[0]
                print_check(tool_name, True, version_string)
                available_tools_count += 1
            else:
                print_check(tool_name, False, "Command failed")
        except (subprocess.SubprocessError, FileNotFoundError):
            print_check(tool_name, False, "Not installed")
    
    return available_tools_count > 0


def main():
    """Main system check function"""
    print("\n" + "=" * 60)
    print("  SYSTEM CHECK - automatic-eureka")
    print("=" * 60)
    
    check_results = []
    
    # Run all checks
    check_results.append(("System Information", check_system_info()))
    check_results.append(("Python Environment", check_python_version()))
    check_results.append(("Git Repository", check_git_repository()))
    check_results.append(("File System", check_file_system()))
    check_results.append(("Development Tools", check_common_tools()))
    
    # Summary
    print_header("Summary")
    passed_checks_count = sum(1 for _, check_passed in check_results if check_passed)
    total_checks_count = len(check_results)
    
    print(f"\nChecks Passed: {passed_checks_count}/{total_checks_count}")
    
    for check_name, check_passed in check_results:
        print_check(check_name, check_passed)
    
    # Exit with appropriate code
    if passed_checks_count == total_checks_count:
        print("\n✓ All system checks passed!\n")
        return 0
    else:
        failed_checks_count = total_checks_count - passed_checks_count
        print(f"\n✗ {failed_checks_count} system check(s) failed.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
