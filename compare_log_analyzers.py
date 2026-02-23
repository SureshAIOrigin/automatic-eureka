"""
Comparison of Log Analyzer Implementations
Demonstrates real-world performance improvements.
"""

import time
from log_analyzer_slow import analyze_logs_slow
from log_analyzer_optimized import analyze_logs_fast


def create_large_test_file(filename, num_entries=10000):
    """Create a large test log file"""
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
    
    with open(filename, 'w') as f:
        iterations = num_entries // 10
        for _ in range(iterations):
            f.write(sample_logs)
    
    print(f"Created test file with ~{num_entries} log entries")


def main():
    """Compare both implementations"""
    print("=" * 80)
    print("LOG ANALYZER PERFORMANCE COMPARISON")
    print("=" * 80)
    
    test_file = '/tmp/large_test_logs.txt'
    create_large_test_file(test_file, num_entries=10000)
    
    print("\n" + "=" * 80)
    print("TESTING INEFFICIENT IMPLEMENTATION")
    print("=" * 80)
    start = time.perf_counter()
    analyzer_slow = analyze_logs_slow(test_file)
    slow_time = time.perf_counter() - start
    
    print("\n" + "=" * 80)
    print("TESTING OPTIMIZED IMPLEMENTATION")
    print("=" * 80)
    start = time.perf_counter()
    analyzer_fast = analyze_logs_fast(test_file)
    fast_time = time.perf_counter() - start
    
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print(f"Inefficient implementation: {slow_time:.4f}s")
    print(f"Optimized implementation:   {fast_time:.4f}s")
    print(f"Speedup:                    {slow_time/fast_time:.2f}x")
    print(f"Time saved:                 {(slow_time - fast_time):.4f}s ({(1 - fast_time/slow_time)*100:.1f}% faster)")
    
    print("\n" + "=" * 80)
    print("KEY OPTIMIZATIONS APPLIED")
    print("=" * 80)
    print("""
1. ✓ Compiled regex patterns once (not on every call)
2. ✓ Used set for user tracking (O(1) instead of O(n) lookups)
3. ✓ Single-pass processing (load + parse + categorize + extract)
4. ✓ Line-by-line file reading (generator pattern for memory efficiency)
5. ✓ Used Counter for efficient counting
6. ✓ Used join() for string building instead of +=
7. ✓ List comprehensions for filtering
8. ✓ Cached parsed results to avoid re-parsing

Impact:
- Reduced time complexity from O(n²) to O(n) for user extraction
- Reduced number of passes through data from 4 to 1
- Reduced memory usage by using generators
- Eliminated regex recompilation overhead
    """)


if __name__ == "__main__":
    main()
