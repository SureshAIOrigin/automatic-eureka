"""
Profiling Example
Demonstrates how to use Python's built-in profiling tools to identify bottlenecks.
"""

import cProfile
import pstats
import io
from examples_inefficient import (
    build_large_string_slow,
    find_duplicates_slow,
    find_common_elements_slow
)
from examples_efficient import (
    build_large_string_fast,
    find_duplicates_fast,
    find_common_elements_fast
)


def profile_function(func, *args, **kwargs):
    """Profile a function and return statistics"""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()
    
    # Get statistics
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result, s.getvalue()


def compare_implementations():
    """Compare inefficient vs efficient implementations with profiling"""
    print("=" * 80)
    print("PROFILING COMPARISON")
    print("=" * 80)
    
    # Test data
    test_items = list(range(5000))
    list1 = list(range(3000))
    list2 = list(range(1500, 4500))
    items_with_dupes = list(range(500)) * 3
    
    # Test 1: String Concatenation
    print("\n1. STRING CONCATENATION")
    print("-" * 80)
    print("INEFFICIENT VERSION:")
    _, profile_out = profile_function(build_large_string_slow, test_items)
    print(profile_out[:500])  # Print first 500 chars
    
    print("\nEFFICIENT VERSION:")
    _, profile_out = profile_function(build_large_string_fast, test_items)
    print(profile_out[:500])
    
    # Test 2: Find Duplicates
    print("\n2. FIND DUPLICATES")
    print("-" * 80)
    print("INEFFICIENT VERSION (nested loops):")
    _, profile_out = profile_function(find_duplicates_slow, items_with_dupes)
    print(profile_out[:500])
    
    print("\nEFFICIENT VERSION (Counter):")
    _, profile_out = profile_function(find_duplicates_fast, items_with_dupes)
    print(profile_out[:500])
    
    # Test 3: Common Elements
    print("\n3. FIND COMMON ELEMENTS")
    print("-" * 80)
    print("INEFFICIENT VERSION (nested iteration):")
    _, profile_out = profile_function(find_common_elements_slow, list1, list2)
    print(profile_out[:500])
    
    print("\nEFFICIENT VERSION (set intersection):")
    _, profile_out = profile_function(find_common_elements_fast, list1, list2)
    print(profile_out[:500])


def demonstrate_line_profiler():
    """Show how to use line_profiler (if available)"""
    print("\n" + "=" * 80)
    print("LINE PROFILER USAGE")
    print("=" * 80)
    print("""
To use line_profiler for detailed line-by-line analysis:

1. Install: pip install line_profiler

2. Add @profile decorator to functions you want to profile:
   @profile
   def my_function():
       # code here
       pass

3. Run with kernprof:
   kernprof -l -v your_script.py

Example output shows time spent on each line:
  Line #      Hits         Time  Per Hit   % Time  Line Contents
  ================================================================
       1                                           def slow_func():
       2      1000      50000.0     50.0     45.5      x = sum(range(100))
       3      1000      60000.0     60.0     54.5      y = sum(range(200))
       4      1000        100.0      0.1      0.0      return x + y
    """)


def demonstrate_memory_profiler():
    """Show how to use memory_profiler (if available)"""
    print("\n" + "=" * 80)
    print("MEMORY PROFILER USAGE")
    print("=" * 80)
    print("""
To track memory usage:

1. Install: pip install memory_profiler

2. Add @profile decorator:
   from memory_profiler import profile
   
   @profile
   def memory_intensive():
       large_list = [0] * (10 ** 6)
       return sum(large_list)

3. Run with:
   python -m memory_profiler your_script.py

Example output:
  Line #    Mem usage    Increment  Occurrences   Line Contents
  =============================================================
       1     38.2 MiB     38.2 MiB           1   def memory_intensive():
       2     76.3 MiB     38.1 MiB           1       large_list = [0] * (10 ** 6)
       3     76.3 MiB      0.0 MiB           1       return sum(large_list)
    """)


def demonstrate_timeit():
    """Show how to use timeit for micro-benchmarking"""
    import timeit
    
    print("\n" + "=" * 80)
    print("TIMEIT USAGE")
    print("=" * 80)
    
    # Compare string concatenation
    setup = "items = list(range(100))"
    
    slow_code = """
result = ""
for item in items:
    result += str(item) + ", "
"""
    
    fast_code = """
result = ", ".join(str(item) for item in items)
"""
    
    slow_time = timeit.timeit(slow_code, setup=setup, number=10000)
    fast_time = timeit.timeit(fast_code, setup=setup, number=10000)
    
    print(f"\nString Concatenation Comparison (10,000 runs):")
    print(f"  Inefficient (+=):  {slow_time:.4f}s")
    print(f"  Efficient (join): {fast_time:.4f}s")
    print(f"  Speedup: {slow_time/fast_time:.2f}x")
    
    # Compare list operations
    setup2 = "numbers = list(range(-100, 100))"
    
    slow_code2 = """
result = []
for num in numbers:
    if num > 0:
        result.append(num * 2)
"""
    
    fast_code2 = """
result = [num * 2 for num in numbers if num > 0]
"""
    
    slow_time2 = timeit.timeit(slow_code2, setup=setup2, number=10000)
    fast_time2 = timeit.timeit(fast_code2, setup=setup2, number=10000)
    
    print(f"\nList Comprehension Comparison (10,000 runs):")
    print(f"  Inefficient (loop):        {slow_time2:.4f}s")
    print(f"  Efficient (comprehension): {fast_time2:.4f}s")
    print(f"  Speedup: {slow_time2/fast_time2:.2f}x")


if __name__ == "__main__":
    compare_implementations()
    demonstrate_timeit()
    demonstrate_line_profiler()
    demonstrate_memory_profiler()
    
    print("\n" + "=" * 80)
    print("PROFILING TIPS")
    print("=" * 80)
    print("""
1. Always profile before optimizing - don't guess where the bottleneck is
2. Use cProfile for overall function-level profiling
3. Use line_profiler for detailed line-by-line analysis
4. Use memory_profiler to find memory leaks or inefficiencies
5. Use timeit for precise micro-benchmarks of small code snippets
6. Focus on the biggest bottlenecks first (80/20 rule)
7. Consider algorithmic complexity (O(n) vs O(n²)) before micro-optimizations
8. Measure the actual impact of your optimizations
    """)
