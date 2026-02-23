"""
Efficient Code Examples
These examples demonstrate optimized versions of common operations.
Use these patterns for better performance.
"""

import time
from collections import defaultdict, Counter
from functools import lru_cache
import copy


# Example 1: Efficient String Concatenation
def build_large_string_fast(items):
    """Efficient: Single join operation"""
    return ", ".join(str(item) for item in items)


# Example 2: Efficient List Building
def filter_and_transform_fast(numbers):
    """Efficient: List comprehension (C-level optimization)"""
    return [num * 2 for num in numbers if num > 0]


# Example 3: Efficient Dictionary Operations
def count_occurrences_fast(items):
    """Efficient: Using Counter from collections"""
    return Counter(items)


def count_occurrences_fast_alt(items):
    """Efficient alternative: Using defaultdict"""
    counts = defaultdict(int)
    for item in items:
        counts[item] += 1
    return dict(counts)


# Example 4: Efficient Set Operations
def find_common_elements_fast(list1, list2):
    """Efficient: O(n) with set intersection"""
    return list(set(list1) & set(list2))


def find_common_elements_fast_ordered(list1, list2):
    """Efficient: Preserves order from list1"""
    set2 = set(list2)
    return [item for item in list1 if item in set2]


# Example 5: Efficient Duplicate Finding
def find_duplicates_fast(items):
    """Efficient: O(n) with Counter"""
    return [item for item, count in Counter(items).items() if count > 1]


def find_duplicates_fast_alt(items):
    """Efficient alternative: Manual set tracking"""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


# Example 6: Efficient File Reading with Generator
def process_file_fast(filename):
    """Efficient: Generator for memory efficiency"""
    with open(filename, 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                yield stripped.upper()


def process_file_fast_list(filename):
    """Efficient: List comprehension for smaller files"""
    with open(filename, 'r') as f:
        return [line.strip().upper() for line in f if line.strip()]


# Example 7: Caching Expensive Calculations
@lru_cache(maxsize=128)
def expensive_calculation(x, y):
    """Cached expensive function"""
    import math
    return math.sqrt(x**2 + y**2)


def calculate_distances_fast(points, reference):
    """Efficient: Caches calculations and avoids redundant work"""
    import math
    distances = []
    ref_x, ref_y = reference
    
    for point in points:
        dx = point[0] - ref_x
        dy = point[1] - ref_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < 100:
            if distance < 50:  # Reuse already calculated distance
                distances.append(distance)
    return distances


# Example 8: Efficient Deep Copy
def copy_nested_structure_fast(data):
    """Efficient: Use built-in deepcopy"""
    return copy.deepcopy(data)


# Example 9: Local Variable Caching
x_global = 10

def compute_with_locals_fast(items):
    """Efficient: Cache global and repeated calculations in local scope"""
    x_local = x_global  # Cache global lookup
    length = len(items)  # Cache length calculation
    return [item * x_local + length for item in items]


# Example 10: Single-pass Data Filtering
def filter_data_fast(records, min_value, max_value, category):
    """Efficient: Single pass through data"""
    return [
        record for record in records
        if min_value <= record['value'] <= max_value
        and record['category'] == category
    ]


# Example 11: Efficient Batch Processing
def process_in_batches(items, batch_size=1000):
    """Efficient: Process data in batches to optimize memory usage"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield process_batch(batch)


def process_batch(batch):
    """Process a single batch of items"""
    return [item * 2 for item in batch if item > 0]


# Example 12: Efficient Database Query Pattern
class DatabaseOptimized:
    """Example of efficient database operations"""
    
    def get_user_details_fast(self, user_ids):
        """Efficient: Single bulk query"""
        if not user_ids:
            return []
        
        # Batch query with IN clause
        placeholders = ','.join('?' * len(user_ids))
        query = f"SELECT * FROM users WHERE id IN ({placeholders})"
        return self.execute_query(query, *user_ids)
    
    def execute_query(self, query, *params):
        """Mock query execution"""
        return []


# Example 13: Efficient String Formatting
def format_user_info_fast(users):
    """Efficient: f-strings are faster than % or .format()"""
    return [f"{user['name']} ({user['email']})" for user in users]


# Example 14: Efficient Early Exit
def find_first_match_fast(items, condition):
    """Efficient: Returns immediately on first match"""
    for item in items:
        if condition(item):
            return item
    return None


# Example 15: Using itertools for Efficient Iterations
from itertools import chain, islice

def flatten_lists_fast(list_of_lists):
    """Efficient: Using itertools.chain"""
    return list(chain.from_iterable(list_of_lists))


def take_first_n_fast(iterable, n):
    """Efficient: Using itertools.islice"""
    return list(islice(iterable, n))


if __name__ == "__main__":
    # Test data
    test_items = list(range(10000))
    test_numbers = list(range(-5000, 5000))
    
    print("Running efficient implementations...\n")
    
    # Example 1: String concatenation
    start = time.perf_counter()
    result = build_large_string_fast(test_items)
    print(f"String concatenation: {time.perf_counter() - start:.4f}s")
    
    # Example 2: List filtering
    start = time.perf_counter()
    result = filter_and_transform_fast(test_numbers)
    print(f"List filtering: {time.perf_counter() - start:.4f}s")
    
    # Example 3: Dictionary counting
    start = time.perf_counter()
    result = count_occurrences_fast(test_numbers * 10)
    print(f"Dictionary counting (Counter): {time.perf_counter() - start:.4f}s")
    
    # Example 4: Common elements
    list1 = list(range(5000))
    list2 = list(range(2500, 7500))
    start = time.perf_counter()
    result = find_common_elements_fast(list1, list2)
    print(f"Find common elements (set): {time.perf_counter() - start:.4f}s")
    
    # Example 5: Find duplicates
    items_with_dupes = test_numbers[:1000] * 2
    start = time.perf_counter()
    result = find_duplicates_fast(items_with_dupes)
    print(f"Find duplicates (Counter): {time.perf_counter() - start:.4f}s")
    
    # Example 9: Local variable caching
    start = time.perf_counter()
    result = compute_with_locals_fast(test_items)
    print(f"Local variable caching: {time.perf_counter() - start:.4f}s")
    
    # Example 10: Single-pass filtering
    test_records = [
        {'value': i, 'category': 'A' if i % 2 == 0 else 'B'}
        for i in range(10000)
    ]
    start = time.perf_counter()
    result = filter_data_fast(test_records, 100, 5000, 'A')
    print(f"Single-pass filtering: {time.perf_counter() - start:.4f}s")
    
    print("\nAll efficient examples completed!")
