#!/bin/bash
# System Check Script for automatic-eureka repository
# Performs comprehensive system validation and health checks

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

print_header() {
    echo ""
    echo "============================================================"
    echo "  $1"
    echo "============================================================"
}

print_check() {
    local name="$1"
    local status="$2"
    local details="$3"
    
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}✓${NC} $name: PASS"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $name: FAIL"
        ((FAILED++))
    fi
    
    if [ -n "$details" ]; then
        echo "  └─ $details"
    fi
}

check_git_repository() {
    print_header "Git Repository Status"
    
    # Check if git is available
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        print_check "Git Available" "pass" "$GIT_VERSION"
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
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ $? -eq 0 ]; then
        print_check "Current Branch" "pass" "$BRANCH"
    else
        print_check "Current Branch" "fail"
    fi
    
    # Check for uncommitted changes
    STATUS=$(git status --porcelain)
    if [ -z "$STATUS" ]; then
        print_check "Working Directory" "pass" "Clean"
    else
        CHANGE_COUNT=$(echo "$STATUS" | wc -l)
        print_check "Working Directory" "pass" "$CHANGE_COUNT uncommitted changes"
    fi
}

check_file_system() {
    print_header "File System Checks"
    
    # Check if README exists
    if [ -f "README.md" ]; then
        SIZE=$(stat -c%s "README.md" 2>/dev/null || stat -f%z "README.md" 2>/dev/null)
        print_check "README.md" "pass" "Size: $SIZE bytes"
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
    DISK_INFO=$(df -h . | tail -1)
    DISK_USAGE=$(echo "$DISK_INFO" | awk '{print $5}' | sed 's/%//')
    DISK_FREE=$(echo "$DISK_INFO" | awk '{print $4}')
    
    if [ "$DISK_USAGE" -lt 90 ]; then
        print_check "Disk Space" "pass" "$DISK_FREE available"
    else
        print_check "Disk Space" "fail" "Low disk space: only $DISK_FREE available"
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
    
    local tools=("git" "python3" "node" "npm" "docker")
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            VERSION=$("$tool" --version 2>&1 | head -1)
            print_check "$tool" "pass" "$VERSION"
        else
            print_check "$tool" "fail" "Not installed"
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
    TOTAL=$((PASSED + FAILED))
    echo ""
    echo "Checks Passed: $PASSED/$TOTAL"
    
    if [ $FAILED -eq 0 ]; then
        echo -e "\n${GREEN}✓${NC} All system checks passed!\n"
        exit 0
    else
        echo -e "\n${RED}✗${NC} $FAILED system check(s) failed.\n"
        exit 1
    fi
}

main
