import sys
import collections
import logging
import os

class CacheManager:

    def __init__(self):
        self._registered = []

    def register(self, cache):
        self._registered.append(cache)

    def display(self):
        for c in self._registered:
            print(c.info())


GlobalCacheManager = CacheManager()

class LRU:

    def __init__(self, size):
        self.t = "LRU"
        self._size = size
        self._cache = collections.OrderedDict()
        logging.debug("LRU cache created")


    def _check_filled(self):
        return len(self) >= self._size

    def fetch(self, key):
        if key in self._cache:
            logging.debug("Key %s found in cache" % str(key))
            val = self._cache.pop(key)
            self.add(key, val)
            return self._cache[key]
        else:
            logging.debug("Key %s not found in cache" % str(key))
            return None

    def pop(self):
        logging.debug("Popping cache")
        item = self._cache.popitem(last=False)
        logging.debug(str(item))
        return item

    def add(self, key, value):
        if self._check_filled():
            self.pop()
        logging.debug('Adding key "%s"' % str(key))
        self._cache[key] = value

    def __len__(self):
        return sys.getsizeof(self._cache)

    def print(self):
        for x, y in self._cache.items():
            print("Key %s : %s" % (str(x), str(y)))


def memcache(size):

    MIN_SIZE = 1024

    assert size >= MIN_SIZE

    class cacheobject(object):

        def __init__(self, func):
            self.func = func
            self.cache = LRU(size)
            GlobalCacheManager.register(self)

        def __call__(self, value):
            response = self.cache.fetch(value)
            if response is None:
                response = self.func(value)
                self.cache.add(value, response)

            return response

        def info(self):
            return "%s:%s - %s:%d bytes" % (os.path.basename(__file__), self.func.__name__, \
                                            self.cache.t , len(self.cache))

    return cacheobject
