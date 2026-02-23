# Code Performance Optimization Guide

This guide identifies common performance issues and provides practical improvements.

## Table of Contents
1. [String Concatenation](#1-string-concatenation)
2. [List Comprehensions vs Loops](#2-list-comprehensions-vs-loops)
3. [Dictionary Lookups](#3-dictionary-lookups)
4. [File I/O Operations](#4-file-io-operations)
5. [Database Query Optimization](#5-database-query-optimization)
6. [Unnecessary Function Calls](#6-unnecessary-function-calls)
7. [Inefficient Data Structures](#7-inefficient-data-structures)
8. [Nested Loops](#8-nested-loops)

## 1. String Concatenation

**Inefficient:**
```python
def build_large_string(items):
    result = ""
    for item in items:
        result += str(item) + ", "  # Creates new string object each iteration
    return result
```

**Efficient:**
```python
def build_large_string(items):
    return ", ".join(str(item) for item in items)  # Single operation
```

**Improvement:** ~10-100x faster for large lists. String concatenation with `+=` creates a new string object each time, while `join()` pre-allocates memory.

## 2. List Comprehensions vs Loops

**Inefficient:**
```python
def filter_and_transform(numbers):
    result = []
    for num in numbers:
        if num > 0:
            result.append(num * 2)
    return result
```

**Efficient:**
```python
def filter_and_transform(numbers):
    return [num * 2 for num in numbers if num > 0]
```

**Improvement:** ~30% faster. List comprehensions are optimized at the C level in CPython.

## 3. Dictionary Lookups

**Inefficient:**
```python
def count_occurrences(items):
    counts = {}
    for item in items:
        if item in counts:
            counts[item] = counts[item] + 1
        else:
            counts[item] = 1
    return counts
```

**Efficient:**
```python
from collections import defaultdict

def count_occurrences(items):
    counts = defaultdict(int)
    for item in items:
        counts[item] += 1
    return dict(counts)
```

**Even Better:**
```python
from collections import Counter

def count_occurrences(items):
    return Counter(items)
```

**Improvement:** ~50-70% faster. Avoids repeated lookups and uses optimized C implementation.

## 4. File I/O Operations

**Inefficient:**
```python
def read_file_line_by_line(filename):
    with open(filename, 'r') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
    return lines
```

**Efficient:**
```python
def read_file_line_by_line(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]
```

**For Large Files:**
```python
def process_large_file(filename):
    # Generator - doesn't load entire file into memory
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()
```

**Improvement:** List comprehension is faster, and generators save memory for large files.

## 5. Database Query Optimization

**Inefficient:**
```python
def get_user_details(user_ids):
    results = []
    for user_id in user_ids:
        # N queries - N+1 problem
        user = db.query("SELECT * FROM users WHERE id = ?", user_id)
        results.append(user)
    return results
```

**Efficient:**
```python
def get_user_details(user_ids):
    # Single query with IN clause
    placeholders = ','.join('?' * len(user_ids))
    query = f"SELECT * FROM users WHERE id IN ({placeholders})"
    return db.query(query, *user_ids)
```

**Improvement:** ~N times faster. Eliminates the N+1 query problem by using bulk operations.

## 6. Unnecessary Function Calls

**Inefficient:**
```python
def process_items(items):
    result = []
    for i in range(len(items)):  # len() called every iteration in some contexts
        if expensive_check(items[i]):  # Called even when not needed
            result.append(items[i])
    return result
```

**Efficient:**
```python
def process_items(items):
    return [item for item in items if expensive_check(item)]
```

**Even Better with Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_check(item):
    # Expensive computation here
    pass

def process_items(items):
    return [item for item in items if expensive_check(item)]
```

**Improvement:** ~2-5x faster with caching for repeated inputs.

## 7. Inefficient Data Structures

**Inefficient:**
```python
def find_common_elements(list1, list2):
    common = []
    for item in list1:
        if item in list2:  # O(n) lookup for each item
            common.append(item)
    return common
```

**Efficient:**
```python
def find_common_elements(list1, list2):
    set2 = set(list2)  # O(1) lookup
    return [item for item in list1 if item in set2]
```

**Even Better:**
```python
def find_common_elements(list1, list2):
    return list(set(list1) & set(list2))
```

**Improvement:** O(n²) → O(n). Using sets provides O(1) lookup instead of O(n).

## 8. Nested Loops

**Inefficient:**
```python
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates
```

**Efficient:**
```python
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
```

**Even Better:**
```python
from collections import Counter

def find_duplicates(items):
    return [item for item, count in Counter(items).items() if count > 1]
```

**Improvement:** O(n²) → O(n). Eliminates nested loop by using hash-based lookups.

## General Best Practices

1. **Use Built-in Functions:** Python's built-ins are implemented in C and are highly optimized
2. **Avoid Premature Optimization:** Profile first, optimize second
3. **Use Appropriate Data Structures:** Choose the right tool for the job (list, set, dict, deque, etc.)
4. **Lazy Evaluation:** Use generators for large datasets
5. **Caching:** Use `@lru_cache` for expensive, repeated computations
6. **Batch Operations:** Process data in batches rather than one-by-one
7. **Avoid Global Lookups:** Cache frequently used globals in local scope
8. **Use `__slots__`:** For classes with many instances, reduce memory overhead

## Profiling Tools

- **cProfile:** Built-in profiler for Python
- **line_profiler:** Line-by-line profiling
- **memory_profiler:** Track memory usage
- **py-spy:** Sampling profiler for production
- **timeit:** Benchmark small code snippets

```python
# Example: Using cProfile
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# Your code here
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```
