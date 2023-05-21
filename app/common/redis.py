import redis

class Redis:
    def __init__(self, host='localhost', port=6379, pool_size=5):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.connection_pool = None

    def __enter__(self):
        self.connection_pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            max_connections=self.pool_size
        )
        return redis.Redis(connection_pool=self.connection_pool)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection_pool:
            self.connection_pool.disconnect()


if __name__ == "__main__":
    # Example usage
    with Redis(host='localhost', port=6379, pool_size=5) as redis_client:
        # Perform Redis operations
        redis_client.set('mykey', 'myvalue')
        value = redis_client.get('mykey')
