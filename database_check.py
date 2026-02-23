#!/usr/bin/env python3
"""Database checker tool - validates database connectivity."""

import sys
import subprocess
import os


def check_mysql_installed():
    """Check if MySQL is installed."""
    print("Checking if MySQL is installed...")
    try:
        result = subprocess.run(['mysql', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ MySQL is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ MySQL check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ MySQL is not installed: {e}")
        return False


def check_postgres_installed():
    """Check if PostgreSQL is installed."""
    print("Checking if PostgreSQL is installed...")
    try:
        result = subprocess.run(['psql', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ PostgreSQL is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ PostgreSQL check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ PostgreSQL is not installed: {e}")
        return False


def check_mongodb_installed():
    """Check if MongoDB is installed."""
    print("Checking if MongoDB is installed...")
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"✓ MongoDB is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ MongoDB check failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"✗ MongoDB is not installed: {e}")
        return False


def check_db_config_exists():
    """Check if database configuration file exists."""
    print("Checking if database config exists...")
    try:
        config_files = ['database.conf', 'db.config', '.env']
        found = False
        for config_file in config_files:
            if os.path.exists(config_file):
                print(f"✓ Database config found: {config_file}")
                found = True
                break
        if not found:
            print(f"✗ No database config file found")
        return found
    except Exception as e:
        print(f"✗ Error checking config: {e}")
        return False


def main():
    """Main function to run database checks."""
    print("\n=== Database Checker ===\n")
    
    results = []
    results.append(check_mysql_installed())
    results.append(check_postgres_installed())
    results.append(check_mongodb_installed())
    results.append(check_db_config_exists())
    
    print(f"\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total} checks")
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
