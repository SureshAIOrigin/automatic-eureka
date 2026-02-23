"""
Web and API Performance Optimization Examples
"""

import time
import json


# Example 1: Inefficient API Response Building
def build_api_response_slow(users):
    """Inefficient: Multiple string operations and json dumps"""
    response = "{"
    response += '"users": ['
    for i, user in enumerate(users):
        user_json = json.dumps(user)
        response += user_json
        if i < len(users) - 1:
            response += ","
    response += "]}"
    return response


def build_api_response_fast(users):
    """Efficient: Single json.dumps operation"""
    return json.dumps({"users": users})


# Example 2: Inefficient Data Serialization
class User:
    """Example user class"""
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


def serialize_users_slow(users):
    """Inefficient: Manual dictionary building"""
    result = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user.id
        user_dict['name'] = user.name
        user_dict['email'] = user.email
        result.append(user_dict)
    return result


def serialize_users_fast(users):
    """Efficient: Dictionary comprehension or use __dict__"""
    return [{'id': u.id, 'name': u.name, 'email': u.email} for u in users]


def serialize_users_fast_alt(users):
    """Efficient alternative: Use vars() or __dict__"""
    return [vars(u) for u in users]


# Example 3: Inefficient Database Query Pattern
class DatabaseAPI:
    """Example database API"""
    
    def query(self, sql, *params):
        """Simulate query execution"""
        time.sleep(0.001)  # Simulate network latency
        return [{'id': i, 'data': f'result_{i}'} for i in range(10)]


def fetch_user_posts_slow(db, user_ids):
    """Inefficient: N+1 query problem"""
    all_posts = []
    for user_id in user_ids:
        # One query per user
        posts = db.query("SELECT * FROM posts WHERE user_id = ?", user_id)
        all_posts.extend(posts)
    return all_posts


def fetch_user_posts_fast(db, user_ids):
    """Efficient: Single bulk query"""
    if not user_ids:
        return []
    
    placeholders = ','.join('?' * len(user_ids))
    query = f"SELECT * FROM posts WHERE user_id IN ({placeholders})"
    return db.query(query, *user_ids)


# Example 4: Inefficient Response Caching
response_cache_dict = {}

def get_cached_response_slow(key, fetch_func):
    """Inefficient: Manual cache without expiration"""
    if key in response_cache_dict:
        return response_cache_dict[key]
    else:
        result = fetch_func()
        response_cache_dict[key] = result
        return result


from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_response_fast(key, fetch_func_name):
    """Efficient: Using lru_cache (note: limitations with unhashable args)"""
    # In real code, you'd need to handle unhashable arguments differently
    return fetch_func_name


# Example 5: Inefficient JSON Parsing
def parse_json_slow(json_strings):
    """Inefficient: Individual parsing in loop"""
    results = []
    for json_str in json_strings:
        data = json.loads(json_str)
        results.append(data)
    return results


def parse_json_fast(json_strings):
    """Efficient: List comprehension (still individual parsing but faster iteration)"""
    return [json.loads(s) for s in json_strings]


# Example 6: Inefficient Request Validation
def validate_requests_slow(requests):
    """Inefficient: Multiple passes through data"""
    # Check all have 'user_id'
    for req in requests:
        if 'user_id' not in req:
            return False
    
    # Check all have 'action'
    for req in requests:
        if 'action' not in req:
            return False
    
    # Check all user_ids are valid
    for req in requests:
        if req['user_id'] < 0:
            return False
    
    return True


def validate_requests_fast(requests):
    """Efficient: Single pass with all checks"""
    required_fields = {'user_id', 'action'}
    return all(
        required_fields.issubset(req.keys()) and req['user_id'] >= 0
        for req in requests
    )


# Example 7: Inefficient Data Aggregation
def aggregate_metrics_slow(events):
    """Inefficient: Multiple iterations over data"""
    total_duration = 0
    for event in events:
        total_duration += event['duration']
    
    count = 0
    for event in events:
        count += 1
    
    error_count = 0
    for event in events:
        if event['status'] == 'error':
            error_count += 1
    
    return {
        'total_duration': total_duration,
        'count': count,
        'error_count': error_count
    }


def aggregate_metrics_fast(events):
    """Efficient: Single pass through data"""
    total_duration = 0
    error_count = 0
    count = 0
    
    for event in events:
        count += 1
        total_duration += event['duration']
        if event['status'] == 'error':
            error_count += 1
    
    return {
        'total_duration': total_duration,
        'count': count,
        'error_count': error_count
    }


# Example 8: Inefficient Data Transformation
def transform_api_data_slow(records):
    """Inefficient: Multiple transformations with intermediate lists"""
    # Step 1: Extract values
    values = []
    for record in records:
        values.append(record['value'])
    
    # Step 2: Filter
    filtered = []
    for value in values:
        if value > 0:
            filtered.append(value)
    
    # Step 3: Transform
    result = []
    for value in filtered:
        result.append(value * 2)
    
    return result


def transform_api_data_fast(records):
    """Efficient: Single-pass pipeline"""
    return [record['value'] * 2 for record in records if record['value'] > 0]


if __name__ == "__main__":
    # Test API response building
    test_users = [{'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com'} for i in range(100)]
    
    print("Web/API Performance Tests")
    print("=" * 80)
    
    start = time.perf_counter()
    result = build_api_response_slow(test_users)
    slow_time = time.perf_counter() - start
    print(f"API Response Building (slow): {slow_time:.4f}s")
    
    start = time.perf_counter()
    result = build_api_response_fast(test_users)
    fast_time = time.perf_counter() - start
    print(f"API Response Building (fast): {fast_time:.4f}s")
    print(f"Speedup: {slow_time/fast_time:.2f}x\n")
    
    # Test validation
    test_requests = [
        {'user_id': i, 'action': 'view', 'timestamp': time.time()}
        for i in range(1000)
    ]
    
    start = time.perf_counter()
    result = validate_requests_slow(test_requests)
    slow_time = time.perf_counter() - start
    print(f"Request Validation (slow): {slow_time:.4f}s")
    
    start = time.perf_counter()
    result = validate_requests_fast(test_requests)
    fast_time = time.perf_counter() - start
    print(f"Request Validation (fast): {fast_time:.4f}s")
    print(f"Speedup: {slow_time/fast_time:.2f}x\n")
    
    # Test data transformation
    test_records = [{'value': i - 500} for i in range(1000)]
    
    start = time.perf_counter()
    result = transform_api_data_slow(test_records)
    slow_time = time.perf_counter() - start
    print(f"Data Transformation (slow): {slow_time:.4f}s")
    
    start = time.perf_counter()
    result = transform_api_data_fast(test_records)
    fast_time = time.perf_counter() - start
    print(f"Data Transformation (fast): {fast_time:.4f}s")
    print(f"Speedup: {slow_time/fast_time:.2f}x")
