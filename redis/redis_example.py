import redis
import time

# 1. Connect to the Redis server
# (Assuming it is running locally on the default port 6379)
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 2. Simulate a slow database call
def get_user_profile(user_id):
    print("Fetching from slow database...")
    time.sleep(2) # Simulating a 2-second database query
    return f"Profile data for User {user_id}"

# 3. Create a function that uses Redis as a cache
def get_profile_with_cache(user_id):
    cache_key = f"user_profile:{user_id}"
    
    # Check if the data is already in Redis
    cached_data = client.get(cache_key)
    
    if cached_data:
        print("Cache HIT! 🚀")
        return cached_data
        
    print("Cache MISS! 🐢")
    # If not in cache, fetch it from the slow database
    db_data = get_user_profile(user_id)
    
    # Save it to Redis for next time, set it to expire in 5 seconds (ex=5)
    client.set(name=cache_key, value=db_data, ex=5)
    
    return db_data

# --- Testing the Cache ---

print("--- First Call ---")
print(get_profile_with_cache(99)) 
# Output: Cache MISS, waits 2 seconds, saves to Redis.

print("\n--- Second Call (Immediately after) ---")
print(get_profile_with_cache(99)) 
# Output: Cache HIT! Returns instantly.

print("\n--- Waiting 6 seconds... ---")
time.sleep(6)

print("\n--- Third Call (After TTL expired) ---")
print(get_profile_with_cache(99)) 
# Output: Cache MISS. The data expired and was automatically deleted by Redis.