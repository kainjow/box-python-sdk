# coding: utf-8

from __future__ import unicode_literals

from collections import OrderedDict

from typing import Optional


class LRUCache(object):
    def __init__(self, capacity=512):
        # type: (int) -> None
        """
        :param capacity:
            The Maximum number of key-value pairs can be cached.
        """
        super(LRUCache, self).__init__()
        self.capacity = capacity
        self.cache = OrderedDict()  # type: OrderedDict[str, object]

    def get(self, key):
        # type: (str) -> object
        """
        Look up the value in cache using the associated key. Returns the value if found.
        Raises :class:`KeyError` otherwise.

        :param key:
            The key used to look up the cache.
        :return:
            The value associated with the key if exists.
        :raises:
            :class:`KeyError` if the key doesn't exist.
        """
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def set(self, key, value=None):
        # type: (str, Optional[object]) -> None
        """
        Store the key-value pair to cache.

        :param key:
            The key associated with the value to be stored. It's used to look up the cache.
        :param value:
            The value to be stored.
        """
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value
