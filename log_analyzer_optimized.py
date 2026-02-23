"""
Real-World Example: Log Analyzer (AFTER Optimization)

This is an optimized version of the log analyzer with all performance improvements applied.
Compare with log_analyzer_slow.py to see the improvements.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime


class LogAnalyzerOptimized:
    """Analyzes application logs - OPTIMIZED VERSION"""
    
    def __init__(self):
        self.log_pattern = re.compile(r'\[(.*?)\] (\w+): (.*)')  # FIX: Compile regex once
        self.user_pattern = re.compile(r'User (\w+)')  # FIX: Compile regex once
        self.parsed_logs = []
        self.errors = []
        self.warnings = []
        self.users = set()  # FIX: Use set for O(1) lookups
    
    def load_and_parse_logs(self, filename):
        """
        Load and parse logs in single pass - OPTIMIZED
        FIX: Use generator to process line by line, combine loading and categorization
        """
        with open(filename, 'r') as f:
            for line in f:  # FIX: Process line by line, not all at once
                if not line.strip():
                    continue
                
                entry = self._parse_log_entry(line)
                if entry:
                    self.parsed_logs.append(entry)
                    
                    # FIX: Categorize in same pass
                    if entry['level'] == 'ERROR':
                        self.errors.append(entry)
                    elif entry['level'] == 'WARN':
                        self.warnings.append(entry)
                    
                    # FIX: Extract users in same pass
                    user_match = self.user_pattern.search(entry['message'])
                    if user_match:
                        self.users.add(user_match.group(1))  # FIX: set.add() is O(1)
    
    def _parse_log_entry(self, log_line):
        """
        Parse a single log entry - OPTIMIZED
        FIX: Use pre-compiled regex pattern
        """
        match = self.log_pattern.match(log_line)  # FIX: Uses pre-compiled pattern
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }
        return None
    
    def count_error_types(self):
        """
        Count different error types - OPTIMIZED
        FIX: Use Counter for efficient counting
        """
        error_messages = (
            error['message'].split(':')[0] if ':' in error['message'] else 'Unknown'
            for error in self.errors
        )
        return Counter(error_messages)
    
    def get_errors_by_user(self, username):
        """
        Get all errors for a user - OPTIMIZED
        FIX: Filter already-parsed logs, use list comprehension
        """
        search_str = f'User {username}'
        return [
            error for error in self.errors
            if search_str in error['message']
        ]
    
    def generate_report(self):
        """
        Generate summary report - OPTIMIZED
        FIX: Use join() for string building
        """
        lines = [
            "=" * 50,
            "LOG ANALYSIS REPORT",
            "=" * 50,
            f"Total logs: {len(self.parsed_logs)}",
            f"Errors: {len(self.errors)}",
            f"Warnings: {len(self.warnings)}",
            f"Unique users: {len(self.users)}",
            "-" * 50,
            "Error Types:"
        ]
        
        error_types = self.count_error_types()
        lines.extend(f"  {error_type}: {count}" for error_type, count in error_types.items())
        
        return "\n".join(lines)  # FIX: Single join operation
    
    def find_patterns(self, pattern_str):
        """
        Find logs matching pattern - OPTIMIZED
        FIX: Compile pattern once, use already-parsed data
        """
        pattern = re.compile(pattern_str)  # FIX: Compile once
        return [
            log for log in self.parsed_logs
            if pattern.search(log['message'])
        ]
    
    def get_statistics(self):
        """
        Get comprehensive statistics - OPTIMIZED
        FIX: Single pass aggregation
        """
        level_counts = Counter(log['level'] for log in self.parsed_logs)
        
        return {
            'total_logs': len(self.parsed_logs),
            'level_counts': dict(level_counts),
            'unique_users': len(self.users),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }


def analyze_logs_fast(filename):
    """Main analysis function - uses optimized implementation"""
    analyzer = LogAnalyzerOptimized()
    
    print("Loading and analyzing logs...")
    analyzer.load_and_parse_logs(filename)  # FIX: Single pass for all operations
    
    print("Generating report...")
    report = analyzer.generate_report()
    print(report)
    
    return analyzer


if __name__ == "__main__":
    import sys
    import time
    
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
    with open('/tmp/sample_logs_optimized.txt', 'w') as f:
        # Write sample logs multiple times to make it substantial
        for _ in range(100):
            f.write(sample_logs)
    
    print("Analyzing logs with OPTIMIZED implementation...")
    print("=" * 80)
    start = time.perf_counter()
    analyzer = analyze_logs_fast('/tmp/sample_logs_optimized.txt')
    elapsed = time.perf_counter() - start
    print(f"\nTotal time: {elapsed:.4f}s")
    print(f"Found {len(analyzer.users)} unique users")
    
    # Show statistics
    stats = analyzer.get_statistics()
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
