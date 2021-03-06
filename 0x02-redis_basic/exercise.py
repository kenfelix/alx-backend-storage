#!/usr/bin/env python3
"""
Module contains a Cache class
"""
import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ memorize user actions"""
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ function  wrapped """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper

def count_calls(method: Callable) -> Callable:
    """ COunts how many times the cache methods are called"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """wrapped function"""
        self._redis.incr(method_key)
        return method(self, *args, **kwds)
    return wrapper

def replay(method: Callable):
    """ display the history call """
    method_key = method.__qualname__
    inputs = method_key + ":inputs"
    outputs = method_key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(method_key).decode("utf-8")
    print("{} was called {} times:".format(method_key, count))
    ListInput = redis.lrange(inputs, 0, -1)
    ListOutput = redis.lrange(outputs, 0, -1)
    allData = list(zip(ListInput, ListOutput))
    for key, data in allData:
        attr, data = key.decode("utf-8"), data.decode("utf-8")
        print("{}(*{}) -> {}".format(method_key, attr, data))

class Cache:
    """A Cache class"""

    def __init__(self):
        """instantiates the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores key value in redis server"""
        randKey = str(uuid4())
        self._redis.mset({randKey: data})
        return randKey

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ get the element and return the decoded version"""
        data = self._redis.get(key)
        if (fn is not None):
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """parametrize Cache.get with the correct conversion function"""
        return data.decode('utf-8')

    def get_int(self, data: str) -> int:
        """parametrize Cache.get with the correct conversion function"""
        return int(data)
