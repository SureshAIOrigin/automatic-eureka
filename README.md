# automatic-eureka
SSSAIO-SAO-SSO-Auto-Eur

## System Check

This repository includes comprehensive system check scripts to validate the environment and repository health.

### Available Scripts

#### Python Version
```bash
python3 system_check.py
```

#### Bash Version
```bash
./system_check.sh
```

### What is Checked

The system check scripts perform the following validations:

1. **System Information**: Display platform, architecture, hostname, and timestamp
2. **Python Environment**: Verify Python version
3. **Git Repository Status**:
   - Git availability and version
   - Repository validity
   - Current branch
   - Working directory status (uncommitted changes)
4. **File System Checks**:
   - README.md existence and size
   - Directory permissions (read, write, execute)
   - Available disk space
5. **Development Tools**: Check availability of common tools:
   - git
   - python3
   - node
   - npm
   - docker

### Exit Codes

- `0`: All checks passed
- `1`: One or more checks failed

### Example Output

```
============================================================
  SYSTEM CHECK - automatic-eureka
============================================================

============================================================
  System Information
============================================================
Platform: Linux 6.11.0-1018-azure
Architecture: x86_64
...

✓ All system checks passed!
```
