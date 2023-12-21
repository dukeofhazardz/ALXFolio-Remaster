from django.db import models
from httpx import AsyncClient, ReadTimeout
from datetime import timedelta
import redis.asyncio as redis
import json


class AysncRedisClient:
    """ The RedisClient Class
    """
    def __init__(self):
        """ Instantiates the RedisClient
        """
        self.connection = None

    async def connect(self):
        """ Instantiates the RedisClient
        """
        self.connection = await redis.from_url(
            'redis://localhost'
        )

    async def close(self):
        """ Closes the connection to Redis
        """
        await self.connection.close()

    async def get(self, key):
        """ Gets data from the Redis Cache
        """
        value = await self.connection.get(key)
        return value

    async def set(self, key, value, duration=None):
        """ Sets data in the Redis Cache
        """
        await self.connection.set(key, value, ex=duration)


class GithubData:
    """ The GithubData Class
    """

    BASE_URL = "https://api.github.com/users/"

    def __init__(self, username):
        """ Instanciates the GithubData class by getting the Base api url
        """
        self.username = username

    async def get_user(self):
        """ Get user data from Github
        """
        async with AsyncClient() as client:
            try:
                redis_client = AysncRedisClient()
                await redis_client.connect()
                user_data = await redis_client.get(self.username)
                if user_data is None:
                    try:
                        response = await client.get(self.BASE_URL + self.username, timeout=30)
                    except ReadTimeout:
                        return None
                    
                    data = None
                    if response.status_code == 200:
                        data = response.json()
                    if data:
                        await redis_client.set(self.username, json.dumps(data), timedelta(hours=24))
                    return None

                else:
                    user_data = json.loads(user_data)
                    return user_data
            except Exception as e:
                print(e)
            finally:
                if redis_client:
                    await redis_client.close()
    
    async def get_repos(self):
        """ Retrieves the github repos of a user
        """
        async with AsyncClient() as client:
            try:
                redis_client = AysncRedisClient()
                await redis_client.connect()
                user_data = await redis_client.get(self.username + "_repos")
                if user_data is None:
                    try:
                        response = await client.get(self.BASE_URL + self.username + "/repos", timeout=30)
                    except ReadTimeout:
                        return None
                    
                    data = None
                    if response.status_code == 200:
                        data = response.json()
                    if data:
                        await redis_client.set(self.username + "_repos", json.dumps(data), timedelta(hours=24))
                    return None

                else:
                    user_data = json.loads(user_data)
                    return user_data
            except Exception as e:
                print(e)
            finally:
                if redis_client:
                    await redis_client.close()
