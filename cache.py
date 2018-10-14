import sys
import collections
import os
import pickle

from enum import Enum


class CacheI(Enum):
    LRU = "LRU"
    CLOCK = "CLOCK"


class CacheManager:

    def __init__(self):
        self._registered = []

    def register(self, cache):
        self._registered.append(cache)

    def display(self):
        for c in self._registered:
            print(c.info())


GlobalCacheManager = CacheManager()


class Cache:

    def __init__(self, size, style):
        self._size = size
        self._style = style

    def fetch(self, key):
         raise NotImplementedError("missing implementation")

    def add(self, key, value):
         raise NotImplementedError("missing implementation")


class LRU(Cache):
    """Standard least recently used implementation

    LRU is one of the most common implementations of a caching algorithm,
    this implementation relies on the internals of the OrderedDict
    implementation

    Note : The size restriction of the LRU will be enforced, but will
    most likely not use the full space provided, this is cause of the internal
    implmenetation of the dyanmic growth of OrderedDict. OrderedDict will
    grow twice as large after reaching a specific capacity, so we have to monitor
    its capacity, and if it doubles past our requirement we must shrink it
    and set a max size (as we now know an estimated max size).  Shrinking
    of an ordered dict only occurs on an INSERT which is why we must
    rehash into a new dictionary.
    """

    def __init__(self, size):
        """ Initialization of the LRU cache

        Args:
            size (int): max size of the cache in bytes

        """
        super().__init__(size, CacheI.LRU)
        self._cache = collections.OrderedDict()
        self._max_size = -1
        self._hits = 0
        self._misses = 0
        self._resizes = 0


    def fetch(self, key):
        """ Fetches a value from the cache, returns None when key is not there"

        Args:
            key (any): key of value in cache

        Returns:
            returns the value at key in cache, or None if the key does
            not exist.
        """
        if key in self._cache:
            val = self._cache.pop(key)
            self.add(key, val)
            self._hits += 1
            return self._cache[key]
        else:
            self._misses += 1
            return None

    def pop(self):
        item = None
        if len(self._cache) > 0:
            item = self._cache.popitem(last=False)
        return item

    def add(self, key, value):
        if self._check_filled():
            self.pop()
        self._cache[key] = value
        # AS WE KNOW MAX_SIZE NOW AND LETS MAINTAIN IT
        if (len(self) > self._size):
            self._resizes += 1
            self._max_size = len(self._cache) - 2
            new_cache = collections.OrderedDict()
            for k, val in self._cache.items():
                if k != key:
                    new_cache[k] = val
            self._cache = new_cache
            self.add(key, value)

    def __len__(self):

        return sys.getsizeof(self._cache)

    def __str__(self):
        hit_p = 0
        resize_p = 0
        denom = (self._hits + self._misses)
        if denom > 0:
            hit_p = (self._hits / denom) * 100
            resize_p = (self._resizes / self._misses) * 100
        return "%s - %d bytes, %.2f%% hit, %.2f%% resizes" % \
            (self._style, len(self), hit_p, resize_p)

    def print(self):
        for x, y in self._cache.items():
            print("Key %s : %s" % (str(x), str(y)))

    def _check_filled(self):
        if self._max_size > 0:
            return self._max_size <= len(self._cache)

        return len(self) >= self._size


def memcache(size, style=CacheI.LRU):

    MIN_SIZE = 2048

    assert size >= MIN_SIZE

    class cacheobject(object):

        def __init__(self, func):
            self.func = func
            self.style = style
            GlobalCacheManager.register(self)

        def __call__(self, *args):
            value = pickle.dumps(args)
            response = self.cache.fetch(value)
            if response is None:
                response = self.func(*args)
                self.cache.add(value, response)

            return response

        @property
        def style(self):

            return self.cache._style

        @style.setter
        def style(self, val):
            if val == CacheI.LRU:
                self.cache = LRU(size)
            elif val == CacheI.CLOCK:
                self.cache = None

        def info(self):

            return "%s:%s:%s" % (os.path.basename(__file__),
                                 self.func.__name__, str(self.cache))

    return cacheobject
