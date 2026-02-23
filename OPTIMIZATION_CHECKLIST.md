# Code Performance Optimization Checklist

Use this checklist when reviewing code for performance issues.

## General Performance

- [ ] Are you using the right algorithm? (Check Big O complexity)
- [ ] Have you profiled to identify actual bottlenecks?
- [ ] Are you optimizing the right thing? (80/20 rule - focus on hot paths)

## Data Structures

- [ ] Using sets for membership tests instead of lists?
- [ ] Using dicts for key-value lookups instead of linear search?
- [ ] Using deque for queue operations instead of list.pop(0)?
- [ ] Using appropriate collection types (Counter, defaultdict, OrderedDict)?

## Loops and Iterations

- [ ] Can nested loops be replaced with set/dict lookups?
- [ ] Are you using list comprehensions instead of manual loops?
- [ ] Can you use generators for large datasets to save memory?
- [ ] Are you avoiding unnecessary iterations (multiple passes)?
- [ ] Using enumerate() instead of range(len())?
- [ ] Using zip() for parallel iteration?

## String Operations

- [ ] Using join() instead of += for string concatenation in loops?
- [ ] Using f-strings instead of % or .format() for Python 3.6+?
- [ ] Avoiding repeated string operations (e.g., .lower() in loop)?

## Function Calls

- [ ] Caching expensive function results with @lru_cache?
- [ ] Avoiding repeated function calls with same arguments?
- [ ] Caching global variable access in local scope?
- [ ] Using built-in functions instead of manual implementations?

## Database Operations

- [ ] Avoiding N+1 query problems with bulk queries?
- [ ] Using connection pooling?
- [ ] Creating appropriate indexes?
- [ ] Using SELECT only needed columns, not SELECT *?
- [ ] Batching INSERT/UPDATE operations?

## File I/O

- [ ] Using generators for large files?
- [ ] Buffering I/O operations?
- [ ] Using binary mode when appropriate?
- [ ] Closing files properly (using context managers)?

## API and Network

- [ ] Implementing response caching?
- [ ] Using connection pooling?
- [ ] Implementing request batching?
- [ ] Using async I/O for concurrent requests?
- [ ] Compressing large responses?

## Memory Management

- [ ] Using generators instead of lists for large datasets?
- [ ] Using __slots__ for classes with many instances?
- [ ] Avoiding unnecessary data copies?
- [ ] Releasing large objects when no longer needed?

## Concurrency

- [ ] Using multiprocessing for CPU-bound tasks?
- [ ] Using asyncio for I/O-bound tasks?
- [ ] Avoiding GIL contention in Python?
- [ ] Using thread pools appropriately?

## Specific Python Optimizations

- [ ] Using list comprehensions over map/filter when possible?
- [ ] Using set comprehensions and dict comprehensions?
- [ ] Leveraging standard library (collections, itertools, functools)?
- [ ] Using any() and all() for short-circuit evaluation?
- [ ] Using bisect for sorted list operations?

## Red Flags to Watch For

🚨 **Critical Issues**:
- String concatenation with += in loops
- N+1 database query patterns
- Nested loops with O(n²) or worse complexity
- Loading entire large files into memory

⚠️ **Warning Signs**:
- Multiple passes through the same data
- Repeated expensive calculations
- List membership tests in loops
- No caching for expensive operations

ℹ️ **Optimization Opportunities**:
- Using range(len()) instead of enumerate()
- Manual deep copy instead of copy.deepcopy()
- Global variable access in tight loops
- Not using generators for large datasets

## Profiling Commands

```bash
# CPU profiling
python -m cProfile -s cumulative your_script.py

# Line-by-line profiling (requires line_profiler)
kernprof -l -v your_script.py

# Memory profiling (requires memory_profiler)  
python -m memory_profiler your_script.py

# Quick micro-benchmark
python -m timeit "code_to_test"
```

## Before vs After Optimization

When optimizing, always:
1. ✅ Measure performance BEFORE changes
2. ✅ Make ONE optimization at a time
3. ✅ Measure performance AFTER changes
4. ✅ Verify correctness with tests
5. ✅ Document the improvement

## Common Speedup Ranges

- String concatenation: 10-100x
- Nested loops → set operations: 100-1000x
- N+1 queries → bulk queries: 10-100x
- List comprehensions: 1.2-2x
- Caching repeated calculations: 2-1000x (depends on cost)
- Generator for memory: 10-100x memory reduction
