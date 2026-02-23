"""
Advanced Performance Optimization Patterns
Additional techniques for improving code performance.
"""

from functools import wraps, lru_cache
from time import perf_counter
import sys


# Pattern 1: Memoization Decorator
def memoize(func):
    """Custom memoization decorator (use @lru_cache for production)"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper


# Pattern 2: Lazy Property Evaluation
class LazyProperty:
    """Descriptor for lazy property evaluation"""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Calculate value and cache it in instance dict
        value = self.func(instance)
        setattr(instance, self.name, value)
        return value


class DataProcessor:
    """Example using lazy properties"""
    
    def __init__(self, data):
        self.data = data
    
    @LazyProperty
    def expensive_calculation(self):
        """Calculated only once, then cached"""
        return sum(x**2 for x in self.data)


# Pattern 3: Object Pooling
class ObjectPool:
    """Simple object pool for expensive-to-create objects"""
    
    def __init__(self, factory, max_size=10):
        self.factory = factory
        self.max_size = max_size
        self.pool = []
    
    def acquire(self):
        """Get object from pool or create new one"""
        if self.pool:
            return self.pool.pop()
        return self.factory()
    
    def release(self, obj):
        """Return object to pool"""
        if len(self.pool) < self.max_size:
            # Reset object state here if needed
            self.pool.append(obj)


# Pattern 4: Batch Processing with Context Manager
class BatchProcessor:
    """Process items in batches for better performance"""
    
    def __init__(self, batch_size=100, processor=None):
        self.batch_size = batch_size
        self.processor = processor or self._default_processor
        self.batch = []
    
    def add(self, item):
        """Add item to batch"""
        self.batch.append(item)
        if len(self.batch) >= self.batch_size:
            self._flush()
    
    def _flush(self):
        """Process current batch"""
        if self.batch:
            self.processor(self.batch)
            self.batch = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._flush()
    
    def _default_processor(self, batch):
        """Default batch processor"""
        print(f"Processing batch of {len(batch)} items")


# Pattern 5: Performance Timing Decorator
def timing_decorator(func):
    """Decorator to measure function execution time"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    
    return wrapper


# Pattern 6: Generator Pipeline
def read_logs(filename):
    """Generator: Read logs one at a time"""
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                yield line.strip()


def parse_logs(log_lines):
    """Generator: Parse log lines"""
    import re
    pattern = re.compile(r'\[(.*?)\] (\w+): (.*)')
    for line in log_lines:
        match = pattern.match(line)
        if match:
            yield {
                'timestamp': match.group(1),
                'level': match.group(2),
                'message': match.group(3)
            }


def filter_errors(parsed_logs):
    """Generator: Filter only error logs"""
    for log in parsed_logs:
        if log['level'] == 'ERROR':
            yield log


def log_pipeline(filename):
    """Efficient pipeline using generators - memory efficient"""
    return filter_errors(parse_logs(read_logs(filename)))


# Pattern 7: Using __slots__ for Memory Optimization
class UserWithoutSlots:
    """Regular class - each instance has a __dict__"""
    
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


class UserWithSlots:
    """Optimized class - no __dict__, uses __slots__"""
    __slots__ = ['id', 'name', 'email']
    
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


def compare_memory_usage():
    """Compare memory usage of classes with/without __slots__"""
    import sys
    
    # Create instances
    user_regular = UserWithoutSlots(1, "Alice", "alice@example.com")
    user_optimized = UserWithSlots(1, "Alice", "alice@example.com")
    
    # Get sizes
    regular_size = sys.getsizeof(user_regular) + sys.getsizeof(user_regular.__dict__)
    optimized_size = sys.getsizeof(user_optimized)
    
    print(f"Regular class size: {regular_size} bytes")
    print(f"Optimized class size: {optimized_size} bytes")
    print(f"Memory saved: {regular_size - optimized_size} bytes ({(1 - optimized_size/regular_size)*100:.1f}%)")


# Pattern 8: Early Exit Optimization
def find_first_slow(items, predicate):
    """Inefficient: Checks all items even after finding match"""
    matches = [item for item in items if predicate(item)]
    return matches[0] if matches else None


def find_first_fast(items, predicate):
    """Efficient: Returns immediately on first match"""
    for item in items:
        if predicate(item):
            return item
    return None


# Pattern 9: Avoiding Repeated Attribute Access
def calculate_slow(points):
    """Inefficient: Repeated attribute access"""
    import math
    results = []
    for point in points:
        # Access point.x and point.y multiple times
        dist = math.sqrt(point.x * point.x + point.y * point.y)
        results.append(dist)
    return results


def calculate_fast(points):
    """Efficient: Cache attribute access"""
    import math
    results = []
    sqrt = math.sqrt  # Cache function lookup
    for point in points:
        x, y = point.x, point.y  # Cache attribute access
        results.append(sqrt(x * x + y * y))
    return results


# Pattern 10: Dictionary get() with Default
def process_config_slow(config, key):
    """Inefficient: Multiple dictionary lookups"""
    if key in config:
        value = config[key]
    else:
        value = "default_value"
    return value.upper()


def process_config_fast(config, key):
    """Efficient: Single dictionary lookup with default"""
    return config.get(key, "default_value").upper()


if __name__ == "__main__":
    print("=" * 80)
    print("ADVANCED OPTIMIZATION PATTERNS")
    print("=" * 80)
    
    # Test lazy property
    print("\n1. Lazy Property Evaluation")
    print("-" * 80)
    data = list(range(10000))
    processor = DataProcessor(data)
    
    start = perf_counter()
    result1 = processor.expensive_calculation  # Calculated here
    t1 = perf_counter() - start
    
    start = perf_counter()
    result2 = processor.expensive_calculation  # Cached, instant
    t2 = perf_counter() - start
    
    print(f"First access (calculated): {t1:.6f}s")
    print(f"Second access (cached):    {t2:.6f}s")
    print(f"Speedup on cached access:  {t1/t2:.2f}x")
    
    # Test __slots__
    print("\n2. __slots__ Memory Optimization")
    print("-" * 80)
    compare_memory_usage()
    
    # Test early exit
    print("\n3. Early Exit Optimization")
    print("-" * 80)
    test_items = list(range(100000))
    predicate = lambda x: x > 50  # Early in the list
    
    start = perf_counter()
    result = find_first_slow(test_items, predicate)
    slow_time = perf_counter() - start
    
    start = perf_counter()
    result = find_first_fast(test_items, predicate)
    fast_time = perf_counter() - start
    
    print(f"Check all items (slow): {slow_time:.4f}s")
    print(f"Early exit (fast):      {fast_time:.6f}s")
    print(f"Speedup:                {slow_time/fast_time:.2f}x")
    
    # Test batch processing
    print("\n4. Batch Processing Pattern")
    print("-" * 80)
    items = list(range(1000))
    
    def batch_processor(batch):
        """Process items in batch"""
        pass  # Simulate batch processing
    
    with BatchProcessor(batch_size=100, processor=batch_processor) as bp:
        for item in items:
            bp.add(item)
    
    print("Processed 1000 items in batches of 100")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
Advanced patterns demonstrated:
1. Lazy evaluation: Calculate expensive values only when needed
2. __slots__: Reduce memory footprint for classes with many instances
3. Early exit: Stop searching as soon as result is found
4. Batch processing: Group operations for better throughput
5. Memoization: Cache expensive function results
6. Attribute caching: Avoid repeated attribute lookups in loops
7. Generator pipelines: Chain operations without intermediate lists
8. Dictionary get(): Single lookup instead of contains + access
    """)
