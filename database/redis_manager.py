import redis 
import json 

class RedisManager:
    """
    Manager to set and get key value data from Redis
    """
    def __init__(cls, cache_expiry: int = 3600):
        cls.cache = redis.Redis(host="localhost", port=6379)
        cls.cache_expiry = cache_expiry
    
    def set_cache(cls, key, data):
        cls.cache.set(key, json.dumps(data), ex=cls.cache_expiry)

    def get_cache(cls, key):
        cached = cls.cache.get(key)
        return json.loads(cached) if cached else None