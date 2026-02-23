#!/usr/bin/env python3
"""Database checker tool - validates database connectivity."""

import os
from check_utils import run_command_check, print_summary_and_exit


def check_mysql_installed():
    """Check if MySQL is installed."""
    return run_command_check(['mysql', '--version'], 'MySQL')


def check_postgres_installed():
    """Check if PostgreSQL is installed."""
    return run_command_check(['psql', '--version'], 'PostgreSQL')


def check_mongodb_installed():
    """Check if MongoDB is installed."""
    return run_command_check(['mongod', '--version'], 'MongoDB')


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
    
    print_summary_and_exit(results)


if __name__ == "__main__":
    main()
