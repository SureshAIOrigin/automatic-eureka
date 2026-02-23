#!/bin/bash
# System Check Script for automatic-eureka repository
# Performs comprehensive system validation and health checks

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NO_COLOR='\033[0m'

# Counters
PASSED_CHECKS_COUNT=0
FAILED_CHECKS_COUNT=0

print_header() {
    echo ""
    echo "============================================================"
    echo "  $1"
    echo "============================================================"
}

print_check() {
    local check_name="$1"
    local check_status="$2"
    local check_details="$3"
    
    if [ "$check_status" = "pass" ]; then
        echo -e "${GREEN}✓${NO_COLOR} $check_name: PASS"
        ((PASSED_CHECKS_COUNT++))
    else
        echo -e "${RED}✗${NO_COLOR} $check_name: FAIL"
        ((FAILED_CHECKS_COUNT++))
    fi
    
    if [ -n "$check_details" ]; then
        echo "  └─ $check_details"
    fi
}

check_git_repository() {
    print_header "Git Repository Status"
    
    # Check if git is available
    if command -v git &> /dev/null; then
        git_version=$(git --version)
        print_check "Git Available" "pass" "$git_version"
    else
        print_check "Git Available" "fail" "Git not found"
        return 1
    fi
    
    # Check if current directory is a git repository
    if git rev-parse --git-dir &> /dev/null; then
        print_check "Git Repository" "pass" ".git directory found"
    else
        print_check "Git Repository" "fail" "Not a git repository"
        return 1
    fi
    
    # Check current branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ $? -eq 0 ]; then
        print_check "Current Branch" "pass" "$current_branch"
    else
        print_check "Current Branch" "fail"
    fi
    
    # Check for uncommitted changes
    git_status_output=$(git status --porcelain)
    if [ -z "$git_status_output" ]; then
        print_check "Working Directory" "pass" "Clean"
    else
        change_count=$(echo "$git_status_output" | wc -l)
        print_check "Working Directory" "pass" "$change_count uncommitted changes"
    fi
}

check_file_system() {
    print_header "File System Checks"
    
    # Check if README exists
    if [ -f "README.md" ]; then
        file_size=$(stat -c%s "README.md" 2>/dev/null || stat -f%z "README.md" 2>/dev/null)
        print_check "README.md" "pass" "Size: $file_size bytes"
    else
        print_check "README.md" "fail" "File not found"
    fi
    
    # Check directory permissions
    if [ -r "." ] && [ -w "." ] && [ -x "." ]; then
        print_check "Directory Permissions" "pass" "Read, Write, Execute OK"
    else
        print_check "Directory Permissions" "fail"
    fi
    
    # Check disk space
    disk_info=$(df -h . | tail -1)
    disk_usage_percent=$(echo "$disk_info" | awk '{print $5}' | sed 's/%//')
    disk_free_space=$(echo "$disk_info" | awk '{print $4}')
    
    if [ "$disk_usage_percent" -lt 90 ]; then
        print_check "Disk Space" "pass" "$disk_free_space available"
    else
        print_check "Disk Space" "fail" "Low disk space: only $disk_free_space available"
    fi
}

check_system_info() {
    print_header "System Information"
    
    echo "Platform: $(uname -s) $(uname -r)"
    echo "Architecture: $(uname -m)"
    echo "Hostname: $(hostname)"
    echo "Current Directory: $(pwd)"
    echo "User: $(whoami)"
    echo "Timestamp: $(date -Iseconds)"
}

check_common_tools() {
    print_header "Development Tools"
    
    local tools_list=("git" "python3" "node" "npm" "docker")
    
    for tool_name in "${tools_list[@]}"; do
        if command -v "$tool_name" &> /dev/null; then
            tool_version=$("$tool_name" --version 2>&1 | head -1)
            print_check "$tool_name" "pass" "$tool_version"
        else
            print_check "$tool_name" "fail" "Not installed"
        fi
    done
}

main() {
    echo ""
    echo "============================================================"
    echo "  SYSTEM CHECK - automatic-eureka"
    echo "============================================================"
    
    # Run all checks
    check_system_info
    check_git_repository
    check_file_system
    check_common_tools
    
    # Summary
    print_header "Summary"
    total_checks_count=$((PASSED_CHECKS_COUNT + FAILED_CHECKS_COUNT))
    echo ""
    echo "Checks Passed: $PASSED_CHECKS_COUNT/$total_checks_count"
    
    if [ $FAILED_CHECKS_COUNT -eq 0 ]; then
        echo -e "\n${GREEN}✓${NO_COLOR} All system checks passed!\n"
        exit 0
    else
        echo -e "\n${RED}✗${NO_COLOR} $FAILED_CHECKS_COUNT system check(s) failed.\n"
        exit 1
    fi
}

main
