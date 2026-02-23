"""
Inefficient Code Examples
These examples demonstrate common performance anti-patterns.
DO NOT use these patterns in production code.
"""

import time


# Example 1: Inefficient String Concatenation
def build_large_string_slow(items):
    """Inefficient: Creates new string object on each iteration"""
    result = ""
    for item in items:
        result += str(item) + ", "
    return result.rstrip(", ")


# Example 2: Inefficient List Building
def filter_and_transform_slow(numbers):
    """Inefficient: Manual loop instead of list comprehension"""
    result = []
    for num in numbers:
        if num > 0:
            result.append(num * 2)
    return result


# Example 3: Inefficient Dictionary Operations
def count_occurrences_slow(items):
    """Inefficient: Multiple dictionary lookups per iteration"""
    counts = {}
    for item in items:
        if item in counts:
            counts[item] = counts[item] + 1
        else:
            counts[item] = 1
    return counts


# Example 4: Inefficient List Membership Check
def find_common_elements_slow(list1, list2):
    """Inefficient: O(n²) complexity - nested linear searches"""
    common = []
    for item in list1:
        if item in list2:  # O(n) lookup for lists
            if item not in common:  # Another O(n) lookup
                common.append(item)
    return common


# Example 5: Nested Loop Inefficiency
def find_duplicates_slow(items):
    """Inefficient: O(n²) nested loops"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates


# Example 6: Inefficient File Reading
def process_file_slow(filename):
    """Inefficient: Loads entire file into memory unnecessarily"""
    with open(filename, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        result = []
        for line in lines:
            if line.strip():
                result.append(line.strip().upper())
    return result


# Example 7: Repeated Expensive Calculations
def calculate_distances_slow(points, reference):
    """Inefficient: Repeats expensive sqrt calculation"""
    import math
    distances = []
    for point in points:
        # Calculate distance multiple times if needed elsewhere
        dx = point[0] - reference[0]
        dy = point[1] - reference[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance < 100:
            # Recalculate for comparison
            dx = point[0] - reference[0]
            dy = point[1] - reference[1]
            if math.sqrt(dx**2 + dy**2) < 50:
                distances.append(distance)
    return distances


# Example 8: Inefficient Deep Copy
def copy_nested_structure_slow(data):
    """Inefficient: Manual deep copy implementation"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = copy_nested_structure_slow(value)
        return result
    elif isinstance(data, list):
        result = []
        for item in data:
            result.append(copy_nested_structure_slow(item))
        return result
    else:
        return data


# Example 9: Global Variable Access in Loop
x_global = 10

def compute_with_globals_slow(items):
    """Inefficient: Repeated global variable lookups"""
    result = []
    for item in items:
        result.append(item * x_global + len(items))  # Global lookup each time
    return result


# Example 10: Inefficient Data Filtering
def filter_data_slow(records, min_value, max_value, category):
    """Inefficient: Multiple passes through data"""
    # First filter by min_value
    filtered1 = []
    for record in records:
        if record['value'] >= min_value:
            filtered1.append(record)
    
    # Then filter by max_value
    filtered2 = []
    for record in filtered1:
        if record['value'] <= max_value:
            filtered2.append(record)
    
    # Finally filter by category
    filtered3 = []
    for record in filtered2:
        if record['category'] == category:
            filtered3.append(record)
    
    return filtered3


if __name__ == "__main__":
    # Test data
    test_items = list(range(10000))
    test_numbers = list(range(-5000, 5000))
    
    # Example 1: String concatenation
    start = time.perf_counter()
    result = build_large_string_slow(test_items)
    print(f"String concatenation: {time.perf_counter() - start:.4f}s")
    
    # Example 2: List filtering
    start = time.perf_counter()
    result = filter_and_transform_slow(test_numbers)
    print(f"List filtering: {time.perf_counter() - start:.4f}s")
    
    # Example 3: Dictionary counting
    start = time.perf_counter()
    result = count_occurrences_slow(test_numbers * 10)
    print(f"Dictionary counting: {time.perf_counter() - start:.4f}s")
    
    # Example 4: Common elements
    list1 = list(range(5000))
    list2 = list(range(2500, 7500))
    start = time.perf_counter()
    result = find_common_elements_slow(list1, list2)
    print(f"Find common elements: {time.perf_counter() - start:.4f}s")
    
    # Example 5: Find duplicates
    items_with_dupes = test_numbers[:1000] * 2
    start = time.perf_counter()
    result = find_duplicates_slow(items_with_dupes)
    print(f"Find duplicates: {time.perf_counter() - start:.4f}s")
