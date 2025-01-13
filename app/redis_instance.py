import redis
from app.config import Config

_redis_instance = None

def get_redis_instance():
    """Get or initialize the Redis instance."""
    global _redis_instance
    if _redis_instance is None:
        _redis_instance = redis.StrictRedis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )
    return _redis_instance