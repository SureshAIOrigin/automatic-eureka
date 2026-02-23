# Quick Reference: Python Performance Optimizations

## When to Use Each Data Structure

| Operation | Inefficient | Efficient | Time Complexity |
|-----------|-------------|-----------|-----------------|
| Membership test | `x in list` | `x in set` | O(n) → O(1) |
| Count items | Manual dict | `Counter(items)` | Similar but cleaner |
| Unique items | `if x not in list` | `set.add(x)` | O(n²) → O(n) |
| Key-value lookup | Linear search | `dict[key]` | O(n) → O(1) |
| Ordered key-value | Manual sorting | `OrderedDict` | Built-in ordering |
| Queue operations | `list.pop(0)` | `deque.popleft()` | O(n) → O(1) |
| Default values | `if key in dict` | `defaultdict(type)` | Cleaner + faster |

## String Operations

```python
# ❌ Slow: O(n²) with repeated string copies
result = ""
for item in items:
    result += str(item)

# ✅ Fast: O(n) with single join operation
result = "".join(str(item) for item in items)

# ❌ Slow: % formatting or .format()
msg = "Hello, %s! You have %d messages" % (name, count)
msg = "Hello, {}! You have {} messages".format(name, count)

# ✅ Fast: f-strings (Python 3.6+)
msg = f"Hello, {name}! You have {count} messages"
```

## Loop Optimizations

```python
# ❌ Slow: range(len())
for i in range(len(items)):
    print(i, items[i])

# ✅ Fast: enumerate
for i, item in enumerate(items):
    print(i, item)

# ❌ Slow: Multiple passes
positives = [x for x in numbers if x > 0]
doubled = [x * 2 for x in positives]

# ✅ Fast: Single pass
doubled = [x * 2 for x in numbers if x > 0]

# ❌ Slow: Nested loops for common elements
common = [x for x in list1 if x in list2]  # O(n²)

# ✅ Fast: Set intersection
common = list(set(list1) & set(list2))  # O(n)
```

## Function Call Optimizations

```python
# ❌ Slow: Repeated function calls
for item in items:
    result.append(expensive_func(item))

# ✅ Fast: Cache with lru_cache
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_func(x):
    # Expensive computation
    return x ** 2

# ❌ Slow: Global variable access in loop
def process():
    for item in items:
        result.append(item * GLOBAL_VAR)

# ✅ Fast: Cache global in local scope
def process():
    local_var = GLOBAL_VAR
    for item in items:
        result.append(item * local_var)
```

## Database Operations

```python
# ❌ Slow: N+1 query problem
posts = []
for user_id in user_ids:
    posts.extend(db.query("SELECT * FROM posts WHERE user_id = ?", user_id))

# ✅ Fast: Bulk query
placeholders = ','.join('?' * len(user_ids))
posts = db.query(f"SELECT * FROM posts WHERE user_id IN ({placeholders})", *user_ids)

# ❌ Slow: Multiple individual inserts
for record in records:
    db.execute("INSERT INTO table VALUES (?, ?)", record.a, record.b)

# ✅ Fast: Batch insert
db.executemany("INSERT INTO table VALUES (?, ?)", 
               [(r.a, r.b) for r in records])
```

## File I/O

```python
# ❌ Slow: Load entire file into memory
with open('large_file.txt') as f:
    content = f.read()
    for line in content.split('\n'):
        process(line)

# ✅ Fast: Process line by line (generator)
with open('large_file.txt') as f:
    for line in f:
        process(line.strip())

# ❌ Slow: Multiple file reads
data1 = open('file.txt').read()
data2 = open('file.txt').read()

# ✅ Fast: Read once, use multiple times
with open('file.txt') as f:
    data = f.read()
    data1 = data
    data2 = data
```

## Regular Expressions

```python
# ❌ Slow: Compile regex on every call
def parse_logs(logs):
    for log in logs:
        match = re.match(r'\[(.*?)\] (\w+): (.*)', log)
        # Process match

# ✅ Fast: Compile once, reuse
import re
LOG_PATTERN = re.compile(r'\[(.*?)\] (\w+): (.*)')

def parse_logs(logs):
    for log in logs:
        match = LOG_PATTERN.match(log)
        # Process match
```

## API and JSON

```python
# ❌ Slow: Manual JSON building
response = "{"
response += '"users": ['
for i, user in enumerate(users):
    response += json.dumps(user)
    if i < len(users) - 1:
        response += ","
response += "]}"

# ✅ Fast: Single json.dumps
response = json.dumps({"users": users})

# ❌ Slow: Multiple validation passes
valid = True
for req in requests:
    if 'user_id' not in req:
        valid = False
for req in requests:
    if 'action' not in req:
        valid = False

# ✅ Fast: Single pass with all()
required = {'user_id', 'action'}
valid = all(required.issubset(req.keys()) for req in requests)
```

## Memory Optimization

```python
# ❌ Memory inefficient: Regular class
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# ✅ Memory efficient: Using __slots__
class User:
    __slots__ = ['id', 'name']
    
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Saves ~60-80% memory per instance for small classes

# ❌ Memory inefficient: Build entire list
results = [process(item) for item in huge_list]

# ✅ Memory efficient: Use generator
results = (process(item) for item in huge_list)
for result in results:
    use(result)
```

## Advanced Techniques

```python
# Lazy evaluation
class DataLoader:
    @property
    def expensive_data(self):
        if not hasattr(self, '_data'):
            self._data = load_expensive_data()
        return self._data

# Early exit
def find_first(items, predicate):
    return next((item for item in items if predicate(item)), None)

# Batch processing
def process_in_batches(items, batch_size=1000):
    for i in range(0, len(items), batch_size):
        yield items[i:i+batch_size]

# Using any() for short-circuit
has_error = any(item.status == 'error' for item in items)  # Stops at first True
```

## Complexity Cheat Sheet

| Pattern | Inefficient | Efficient | Complexity Change |
|---------|-------------|-----------|-------------------|
| Find duplicates | Nested loops | Set tracking | O(n²) → O(n) |
| Common elements | Nested loops | Set intersection | O(n·m) → O(n+m) |
| Membership test | List scan | Set/dict lookup | O(n) → O(1) |
| Count items | Manual dict | Counter | O(n) → O(n) but faster |
| String concat in loop | += | join() | O(n²) → O(n) |
| Multiple filters | N passes | Single pass | N·O(n) → O(n) |

## Profiling Commands

```bash
# CPU profiling
python -m cProfile -s cumulative script.py > profile.txt

# Sort by total time
python -m cProfile -s tottime script.py

# Line-by-line profiling (requires line_profiler)
pip install line_profiler
kernprof -l -v script.py

# Memory profiling (requires memory_profiler)
pip install memory_profiler
python -m memory_profiler script.py

# Quick timing
python -m timeit -n 1000 "code_snippet_here"
```

## Red Flags 🚨

Watch for these patterns in code reviews:
1. `result += str` in a loop
2. `if x in list:` inside a loop
3. Nested `for` loops that could use sets/dicts
4. Multiple passes through same data
5. `re.compile()` inside a loop or function
6. Loading entire large files with `.read()`
7. N+1 database query patterns
8. Creating objects in tight loops

## Golden Rules

1. ✅ Profile before optimizing
2. ✅ Optimize algorithms before micro-optimizations
3. ✅ Use appropriate data structures
4. ✅ Minimize passes through data
5. ✅ Cache expensive operations
6. ✅ Use built-in functions and libraries
7. ✅ Consider memory vs speed tradeoffs
8. ✅ Measure the actual improvement
