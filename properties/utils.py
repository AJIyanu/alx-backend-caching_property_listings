import logging
from django_redis import get_redis_connection
from django.core.cache import cache

# Configure logging
logger = logging.getLogger(__name__)


def get_redis_cache_metrics():
    """
    Get Redis cache metrics including hits, misses, and hit ratio.
    
    Returns:
        dict: A dictionary containing:
            - keyspace_hits (int): Number of successful key lookups
            - keyspace_misses (int): Number of failed key lookups
            - hit_ratio (float): Cache hit ratio (hits / total requests)
            - total_requests (int): Total cache requests (hits + misses)
            - cache_keys (int): Number of keys currently in cache
            - used_memory (str): Memory used by Redis
            - connected_clients (int): Number of connected clients
    """
    try:
        # Get Redis connection
        redis_client = get_redis_connection("default")
        
        # Get Redis INFO statistics
        info = redis_client.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        total_requests = keyspace_hits + keyspace_misses
        
        # Calculate hit ratio (avoid division by zero)
        if total_requests > 0:
            hit_ratio = keyspace_hits / total_requests
        else:
            hit_ratio = 0.0
        
        # Get additional metrics
        cache_keys = redis_client.dbsize()
        used_memory = info.get('used_memory_human', 'N/A')
        connected_clients = info.get('connected_clients', 0)
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'hit_ratio_percentage': round(hit_ratio * 100, 2),
            'cache_keys': cache_keys,
            'used_memory': used_memory,
            'connected_clients': connected_clients,
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics:")
        logger.info(f"  - Keyspace Hits: {keyspace_hits}")
        logger.info(f"  - Keyspace Misses: {keyspace_misses}")
        logger.info(f"  - Total Requests: {total_requests}")
        logger.info(f"  - Hit Ratio: {hit_ratio:.2%}")
        logger.info(f"  - Cache Keys: {cache_keys}")
        logger.info(f"  - Used Memory: {used_memory}")
        logger.info(f"  - Connected Clients: {connected_clients}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'hit_ratio_percentage': 0.0,
            'cache_keys': 0,
            'used_memory': 'N/A',
            'connected_clients': 0,
        }