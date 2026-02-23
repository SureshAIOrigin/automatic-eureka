"""
Real-World Example: Log Analyzer (BEFORE Optimization)

This is a realistic log analysis application with multiple performance issues.
See log_analyzer_optimized.py for the improved version.
"""

import re
import json
from datetime import datetime


class LogAnalyzer:
    """Analyzes application logs - INEFFICIENT VERSION"""
    
    def __init__(self):
        self.logs = []
        self.errors = []
        self.warnings = []
        self.users = []
    
    def load_logs(self, filename):
        """Load logs from file - ISSUE: Loads entire file into memory"""
        with open(filename, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    self.logs.append(line)
    
    def parse_log_entry(self, log_line):
        """Parse a single log entry - ISSUE: Repeated regex compilation"""
        # Compiles regex on every call
        pattern = r'\[(.*?)\] (\w+): (.*)'
        match = re.match(pattern, log_line)
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }
        return None
    
    def categorize_logs(self):
        """Categorize logs by level - ISSUE: Multiple passes through data"""
        # First pass: find errors
        for log in self.logs:
            entry = self.parse_log_entry(log)
            if entry and entry['level'] == 'ERROR':
                self.errors.append(entry)
        
        # Second pass: find warnings
        for log in self.logs:
            entry = self.parse_log_entry(log)
            if entry and entry['level'] == 'WARN':
                self.warnings.append(entry)
    
    def extract_users(self):
        """Extract unique users - ISSUE: O(n²) complexity"""
        for log in self.logs:
            entry = self.parse_log_entry(log)
            if entry:
                # Extract user from message (e.g., "User john logged in")
                user_match = re.search(r'User (\w+)', entry['message'])
                if user_match:
                    user = user_match.group(1)
                    # O(n) lookup on every iteration
                    if user not in self.users:
                        self.users.append(user)
    
    def count_error_types(self):
        """Count different error types - ISSUE: Manual counting instead of Counter"""
        error_types = {}
        for error in self.errors:
            error_type = error['message'].split(':')[0] if ':' in error['message'] else 'Unknown'
            if error_type in error_types:
                error_types[error_type] = error_types[error_type] + 1
            else:
                error_types[error_type] = 1
        return error_types
    
    def get_errors_by_user(self, username):
        """Get all errors for a user - ISSUE: Repeated regex and parsing"""
        user_errors = []
        for log in self.logs:
            entry = self.parse_log_entry(log)
            if entry and entry['level'] == 'ERROR':
                if f'User {username}' in entry['message']:
                    user_errors.append(entry)
        return user_errors
    
    def generate_report(self):
        """Generate summary report - ISSUE: Inefficient string building"""
        report = ""
        report += "=" * 50 + "\n"
        report += "LOG ANALYSIS REPORT\n"
        report += "=" * 50 + "\n"
        report += f"Total logs: {len(self.logs)}\n"
        report += f"Errors: {len(self.errors)}\n"
        report += f"Warnings: {len(self.warnings)}\n"
        report += f"Unique users: {len(self.users)}\n"
        report += "-" * 50 + "\n"
        
        error_types = self.count_error_types()
        report += "Error Types:\n"
        for error_type, count in error_types.items():
            report += f"  {error_type}: {count}\n"
        
        return report
    
    def find_patterns(self, pattern_str):
        """Find logs matching pattern - ISSUE: Repeated regex compilation"""
        matches = []
        for log in self.logs:
            # Compiles regex for every log line
            if re.search(pattern_str, log):
                matches.append(log)
        return matches


def analyze_logs_slow(filename):
    """Main analysis function - orchestrates all inefficient operations"""
    analyzer = LogAnalyzer()
    
    print("Loading logs...")
    analyzer.load_logs(filename)
    
    print("Categorizing logs...")
    analyzer.categorize_logs()
    
    print("Extracting users...")
    analyzer.extract_users()
    
    print("Generating report...")
    report = analyzer.generate_report()
    print(report)
    
    return analyzer


if __name__ == "__main__":
    import sys
    
    # Create sample log file for testing
    sample_logs = """[2024-01-01 10:00:00] INFO: User alice logged in
[2024-01-01 10:00:01] INFO: User bob logged in
[2024-01-01 10:00:02] ERROR: DatabaseError: Connection timeout for User alice
[2024-01-01 10:00:03] WARN: User charlie attempted invalid operation
[2024-01-01 10:00:04] ERROR: AuthError: Invalid token for User bob
[2024-01-01 10:00:05] INFO: User alice logged out
[2024-01-01 10:00:06] ERROR: DatabaseError: Connection timeout for User charlie
[2024-01-01 10:00:07] WARN: Rate limit exceeded for User alice
[2024-01-01 10:00:08] INFO: User bob performed action
[2024-01-01 10:00:09] ERROR: DatabaseError: Query failed for User bob
"""
    
    # Write sample log file
    with open('/tmp/sample_logs.txt', 'w') as f:
        # Write sample logs multiple times to make it substantial
        for _ in range(100):
            f.write(sample_logs)
    
    print("Analyzing logs with INEFFICIENT implementation...")
    print("=" * 80)
    import time
    start = time.perf_counter()
    analyzer = analyze_logs_slow('/tmp/sample_logs.txt')
    elapsed = time.perf_counter() - start
    print(f"\nTotal time: {elapsed:.4f}s")
    print(f"Found {len(analyzer.users)} unique users")
