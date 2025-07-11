import redis

class RedisMemory:
    """
    A simple Redis-based memory system for the AgentAlpha framework.
    """
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initializes a new RedisMemory instance.

        Args:
            host (str, optional): The Redis host. Defaults to 'localhost'.
            port (int, optional): The Redis port. Defaults to 6379.
            db (int, optional): The Redis database. Defaults to 0.
        """
        try:
            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.client.ping()
            print("Successfully connected to Redis.")
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            self.client = None

    def set(self, key, value):
        """
        Stores a key-value pair in Redis.

        Args:
            key (str): The key to store.
            value (any): The value to store.
        """
        if self.client:
            self.client.set(key, value)

    def get(self, key):
        """
        Retrieves a value from Redis by key.

        Args:
            key (str): The key to retrieve.

        Returns:
            any: The value associated with the key, or None if not found or if Redis is not connected.
        """
        if self.client:
            return self.client.get(key)
        return None

    def delete(self, key):
        """
        Deletes a key from Redis.

        Args:
            key (str): The key to delete.
        """
        if self.client:
            self.client.delete(key)
