# automatic-eureka

A collection of system validation and checking tools with refactored, maintainable code.

## Overview

This repository contains three checker tools that validate different aspects of system configuration:

- **system_check.py** - Validates system requirements and installed development tools
- **database_check.py** - Validates database software installations
- **website_checker.py** - Validates website connectivity and network configuration

## Code Refactoring

This repository demonstrates best practices for identifying and eliminating code duplication through refactoring.

### Refactoring Results

**Before Refactoring:**
- Total lines: 324 lines across 3 files
- Duplicated subprocess checking logic in 6 functions
- Duplicated HTTP request logic in 2 functions
- Duplicated summary reporting logic in 3 files

**After Refactoring:**
- Total lines: 280 lines across 4 files (13.6% reduction)
- Single reusable `run_command_check()` function
- Single reusable `check_http_request()` function
- Single reusable `print_summary_and_exit()` function

**Per-File Improvements:**
- database_check.py: 46% reduction (104 → 56 lines)
- system_check.py: 41% reduction (119 → 70 lines)
- website_checker.py: 27% reduction (101 → 74 lines)

### Key Refactoring Patterns

1. **Subprocess Command Pattern** - Extracted common subprocess execution logic into `run_command_check()`
2. **HTTP Request Pattern** - Unified HTTP/HTTPS checking into `check_http_request()`
3. **Results Summary Pattern** - Standardized result reporting with `print_summary_and_exit()`

## Usage

### System Checker
```bash
python3 system_check.py
```

Checks for:
- Git installation
- Python installation
- Node.js installation
- Available disk space
- Write permissions

### Database Checker
```bash
python3 database_check.py
```

Checks for:
- MySQL installation
- PostgreSQL installation
- MongoDB installation
- Database configuration files

### Website Checker
```bash
python3 website_checker.py <url>
```

Checks for:
- HTTP connectivity
- HTTPS connectivity
- DNS resolution
- Port 80 availability
- Port 443 availability

## Testing

Run the test suite to verify the refactored code:
```bash
python3 test_refactored.py
```

## Architecture

All checker tools utilize the shared `check_utils.py` module which provides:

- `run_command_check()` - Generic subprocess command execution and validation
- `check_http_request()` - Generic HTTP/HTTPS request validation
- `print_summary_and_exit()` - Standardized result reporting and exit handling

This modular architecture:
- Eliminates code duplication
- Improves maintainability
- Makes it easy to add new checkers
- Provides consistent error handling and output formatting
