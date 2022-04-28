#!/usr/bin/env python3
"""
Module contains a Cache class
"""
import redis
from uuid import uuid4
from typing import Union

class Cache:
    """A Cache class"""

    def __init__(self):
        """instantiates the class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        randKey = str(uuid4())
        self._redis.mset({randKey: data})
        return randKey
