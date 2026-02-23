"""
Performance Benchmark Comparison
Compares inefficient vs efficient implementations to demonstrate improvements.
"""

import time
import sys
from examples_inefficient import (
    build_large_string_slow,
    filter_and_transform_slow,
    count_occurrences_slow,
    find_common_elements_slow,
    find_duplicates_slow,
)
from examples_efficient import (
    build_large_string_fast,
    filter_and_transform_fast,
    count_occurrences_fast,
    find_common_elements_fast,
    find_duplicates_fast,
    compute_with_locals_fast,
    filter_data_fast,
)


def benchmark(func, *args, runs=3):
    """Run a function multiple times and return average execution time"""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        times.append(time.perf_counter() - start)
    return sum(times) / len(times)


def format_speedup(slow_time, fast_time):
    """Format speedup ratio"""
    if fast_time == 0:
        return "∞"
    speedup = slow_time / fast_time
    return f"{speedup:.2f}x"


def print_comparison(name, slow_time, fast_time):
    """Print formatted comparison"""
    speedup = format_speedup(slow_time, fast_time)
    print(f"{name:40s} | Slow: {slow_time:8.4f}s | Fast: {fast_time:8.4f}s | Speedup: {speedup:>8s}")


def main():
    """Run all benchmarks and display results"""
    print("=" * 100)
    print("PERFORMANCE BENCHMARK RESULTS")
    print("=" * 100)
    print(f"{'Operation':40s} | {'Inefficient':>12s} | {'Efficient':>12s} | {'Speedup':>10s}")
    print("-" * 100)
    
    # Prepare test data
    test_items_small = list(range(1000))
    test_items_medium = list(range(5000))
    test_items_large = list(range(10000))
    test_numbers = list(range(-5000, 5000))
    
    # Benchmark 1: String Concatenation
    slow = benchmark(build_large_string_slow, test_items_small)
    fast = benchmark(build_large_string_fast, test_items_small)
    print_comparison("1. String Concatenation (1K items)", slow, fast)
    
    # Benchmark 2: List Filtering & Transformation
    slow = benchmark(filter_and_transform_slow, test_numbers)
    fast = benchmark(filter_and_transform_fast, test_numbers)
    print_comparison("2. List Filter & Transform (10K items)", slow, fast)
    
    # Benchmark 3: Dictionary Counting
    test_data = test_numbers * 10
    slow = benchmark(count_occurrences_slow, test_data)
    fast = benchmark(count_occurrences_fast, test_data)
    print_comparison("3. Count Occurrences (100K items)", slow, fast)
    
    # Benchmark 4: Finding Common Elements
    list1 = list(range(1000))
    list2 = list(range(500, 1500))
    slow = benchmark(find_common_elements_slow, list1, list2)
    fast = benchmark(find_common_elements_fast, list1, list2)
    print_comparison("4. Find Common Elements (1K each)", slow, fast)
    
    # Benchmark 5: Finding Duplicates
    items_with_dupes = list(range(500)) * 2
    slow = benchmark(find_duplicates_slow, items_with_dupes)
    fast = benchmark(find_duplicates_fast, items_with_dupes)
    print_comparison("5. Find Duplicates (1K items)", slow, fast)
    
    # Benchmark 6: Single-pass Filtering
    test_records = [
        {'value': i, 'category': 'A' if i % 2 == 0 else 'B'}
        for i in range(10000)
    ]
    
    # Simulating inefficient multi-pass
    def filter_multipass(records):
        filtered1 = [r for r in records if r['value'] >= 100]
        filtered2 = [r for r in filtered1 if r['value'] <= 5000]
        filtered3 = [r for r in filtered2 if r['category'] == 'A']
        return filtered3
    
    slow = benchmark(filter_multipass, test_records)
    fast = benchmark(filter_data_fast, test_records, 100, 5000, 'A')
    print_comparison("6. Multi-condition Filter (10K records)", slow, fast)
    
    # Benchmark 7: Local vs Global Variable Access
    x_global = 10
    
    def with_globals(items):
        return [item * x_global + len(items) for item in items]
    
    slow = benchmark(with_globals, test_items_medium)
    fast = benchmark(compute_with_locals_fast, test_items_medium)
    print_comparison("7. Local Variable Caching (5K items)", slow, fast)
    
    print("-" * 100)
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("""
Key Takeaways:
1. String concatenation with join() is significantly faster than += for large strings
2. List comprehensions outperform manual loop building
3. Use Counter or defaultdict for counting operations
4. Convert lists to sets for O(1) membership testing instead of O(n)
5. Avoid nested loops when possible - use sets or dicts for lookups
6. Single-pass filtering is faster than multiple passes
7. Cache global variables and repeated calculations in local scope
8. Use generators for large files to save memory

Performance Optimization Tips:
- Profile before optimizing (use cProfile, line_profiler)
- Choose appropriate data structures (set for membership, dict for lookups)
- Leverage built-in functions and standard library (highly optimized C code)
- Avoid premature optimization - optimize bottlenecks identified through profiling
- Consider memory vs speed tradeoffs
""")


if __name__ == "__main__":
    main()
