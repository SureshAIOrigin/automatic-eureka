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


def print_check(name, status, details=""):
    """Print a check result"""
    status_symbol = "✓" if status else "✗"
    print(f"{status_symbol} {name}: {'PASS' if status else 'FAIL'}")
    if details:
        print(f"  └─ {details}")


def check_python_version():
    """Check Python version"""
    print_header("Python Environment")
    version = sys.version_info
    print_check(
        "Python Version",
        True,
        f"{version.major}.{version.minor}.{version.micro}"
    )
    return True


def check_git_repository():
    """Check Git repository status"""
    print_header("Git Repository Status")
    
    checks_passed = 0
    total_checks = 0
    
    # Check if git is available
    total_checks += 1
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        git_version = result.stdout.strip()
        print_check("Git Available", True, git_version)
        checks_passed += 1
    except (subprocess.SubprocessError, FileNotFoundError):
        print_check("Git Available", False, "Git not found")
        return False
    
    # Check if current directory is a git repository
    total_checks += 1
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print_check("Git Repository", True, ".git directory found")
            checks_passed += 1
        else:
            print_check("Git Repository", False, "Not a git repository")
    except subprocess.SubprocessError:
        print_check("Git Repository", False, "Git command failed")
    
    # Check current branch
    total_checks += 1
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            print_check("Current Branch", True, branch)
            checks_passed += 1
        else:
            print_check("Current Branch", False)
    except subprocess.SubprocessError:
        print_check("Current Branch", False, "Git command failed")
    
    # Check for uncommitted changes
    total_checks += 1
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            has_changes = len(changes) > 0
            print_check(
                "Working Directory",
                True,
                "Clean" if not has_changes else f"{len(changes.splitlines())} uncommitted changes"
            )
            checks_passed += 1
    except subprocess.SubprocessError:
        print_check("Working Directory", False, "Git command failed")
    
    return checks_passed == total_checks


def check_file_system():
    """Check file system and repository structure"""
    print_header("File System Checks")
    
    checks_passed = 0
    total_checks = 0
    
    # Check if README exists
    total_checks += 1
    readme_exists = os.path.isfile("README.md")
    print_check("README.md", readme_exists)
    if readme_exists:
        checks_passed += 1
        # Check README size
        size = os.path.getsize("README.md")
        print(f"  └─ Size: {size} bytes")
    
    # Check directory permissions
    total_checks += 1
    try:
        can_read = os.access(".", os.R_OK)
        can_write = os.access(".", os.W_OK)
        can_execute = os.access(".", os.X_OK)
        
        perms_ok = can_read and can_write and can_execute
        print_check(
            "Directory Permissions",
            perms_ok,
            f"Read: {can_read}, Write: {can_write}, Execute: {can_execute}"
        )
        if perms_ok:
            checks_passed += 1
    except Exception as e:
        print_check("Directory Permissions", False, str(e))
    
    # Check disk space
    total_checks += 1
    try:
        import shutil
        usage = shutil.disk_usage(".")
        free_gb = usage.free / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)
        percent_free = (usage.free / usage.total) * 100
        
        disk_ok = percent_free > 10  # At least 10% free
        print_check(
            "Disk Space",
            disk_ok,
            f"{free_gb:.2f} GB free of {total_gb:.2f} GB ({percent_free:.1f}%)"
        )
        if disk_ok:
            checks_passed += 1
    except Exception as e:
        print_check("Disk Space", False, str(e))
    
    return checks_passed == total_checks


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
    
    tools = [
        ("git", ["git", "--version"]),
        ("python3", ["python3", "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("docker", ["docker", "--version"]),
    ]
    
    available_tools = 0
    
    for tool_name, command in tools:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip().split("\n")[0]
                print_check(tool_name, True, version)
                available_tools += 1
            else:
                print_check(tool_name, False, "Command failed")
        except (subprocess.SubprocessError, FileNotFoundError):
            print_check(tool_name, False, "Not installed")
    
    return available_tools > 0


def main():
    """Main system check function"""
    print("\n" + "=" * 60)
    print("  SYSTEM CHECK - automatic-eureka")
    print("=" * 60)
    
    results = []
    
    # Run all checks
    results.append(("System Information", check_system_info()))
    results.append(("Python Environment", check_python_version()))
    results.append(("Git Repository", check_git_repository()))
    results.append(("File System", check_file_system()))
    results.append(("Development Tools", check_common_tools()))
    
    # Summary
    print_header("Summary")
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    print(f"\nChecks Passed: {passed}/{total}")
    
    for check_name, status in results:
        print_check(check_name, status)
    
    # Exit with appropriate code
    if passed == total:
        print("\n✓ All system checks passed!\n")
        return 0
    else:
        print(f"\n✗ {total - passed} system check(s) failed.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
