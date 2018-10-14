import os
import sys
import collections
import pickle
import time
import curses

from abc import ABC, abstractmethod
from enum import Enum
from texttable import Texttable


class CacheI(Enum):
    LRU = "LRU"
    CLOCK = "CLOCK"


class CacheManager:

    def __init__(self):
        self._registered = []

    def register(self, cache):
        self._registered.append(cache)

    def display(self):
        """ Display will print a table of all the caches in real time

        Note : Run this in a new thread!
        """
        def helper(window):
            window.nodelay(True)
            while (True):
                window.clear()
                table = Texttable()
                table.set_cols_align(["l", "l", "r", "r", "l", "l"])
                rows = [c.info() for c in self._registered]
                final = [["Location", "Cache Type", "Entries",
                        "Size (bytes)", "Hit (%)", "Adds causing resize (%)"]] + rows
                table.add_rows(final)
                window.addstr(table.draw())
                window.refresh()
                c = window.getch()
                if c == ord('q'):
                    break
                time.sleep(0.5)

        curses.wrapper(helper)


GlobalCacheManager = CacheManager()


class Cache(ABC):

    def __init__(self, size, style):
        self._size = size
        self._style = style

    @abstractmethod
    def fetch(self, key):
        raise NotImplementedError("missing implementation")

    @abstractmethod
    def add(self, key, value):
        raise NotImplementedError("missing implementation")

    @abstractmethod
    def info(self):
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

    # @profile
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

    # @profile
    def pop(self):
        """ Pops the least recently used element from the cache"""
        item = None
        if len(self._cache) > 0:
            item = self._cache.popitem(last=False)
        return item

    # @profile
    def add(self, key, value):
        """ Adds a key and value pair to the cache

        Note : This sometimes forces a resize of the cache, this occurs
        rarely but its around to make sure we enforce the size restriction
        set by the user


        Args:
            key (any) : The key of the cache entry
            value (any): The value to be inserted at they key
        """
        if self._check_filled():
            self.pop()
        self._cache[key] = value
        if (self.bsize() > self._size):
            self._resizes += 1
            self._max_size = len(self._cache) - 2
            new_cache = collections.OrderedDict()
            for k, val in self._cache.items():
                if k != key:
                    new_cache[k] = val
            self._cache = new_cache
            self.add(key, value)

    def bsize(self):
        """ Byte size of our cache object """
        sizeof = sys.getsizeof
        size = sizeof(self._hits)
        size += sizeof(self._size)
        size += sizeof(self._hits)
        size += sizeof(self._style)
        size += sizeof(self._misses)
        size += sizeof(self._resizes)
        size += sizeof(self._cache)

        return size

    def info(self):
        hit_p = 0
        resize_p = 0
        denom = (self._hits + self._misses)
        if denom > 0:
            hit_p = (self._hits / denom) * 100
            resize_p = (self._resizes / self._misses) * 100
        return [self._style, len(self), self.bsize(), hit_p, resize_p]

    def __len__(self):

        return len(self._cache)

    def __str__(self):
        hit_p = 0
        resize_p = 0
        denom = (self._hits + self._misses)
        if denom > 0:
            hit_p = (self._hits / denom) * 100
            resize_p = (self._resizes / self._misses) * 100
        return "%s - %d entries, %d bytes, %.2f%% hit, %.2f%% adds cause resize" % \
            (self._style, len(self), self.bsize(), hit_p, resize_p)

    def print(self):
        """ Prints all cache entries in the cache"""
        for x, y in self._cache.items():
            print("Key %s : %s" % (str(x), str(y)))

    def _check_filled(self):
        if self._max_size > 0:
            return self._max_size <= len(self)

        return self.bsize() >= self._size


def memcache(size, style=CacheI.LRU):
    """Decorator caching object for functions


    """
    MIN_SIZE = 2048

    assert size >= MIN_SIZE

    class cacheobject(object):

        def __init__(self, func):
            self.func = func
            self.style = style
            GlobalCacheManager.register(self)

        # @profile
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
            info = []
            info.append(
                "%s:%s" %
                (os.path.basename(__file__),
                 self.func.__name__))
            info.extend(self.cache.info())

            return info

    return cacheobject
