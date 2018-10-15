import time
import curses

from abc import ABC, abstractmethod
from enum import Enum
from texttable import Texttable


class CacheI(Enum):
    LRU = 1
    CLOCK = 2
    ARC = 3
    FIFO = 4


class CacheManager:

    def __init__(self):
        self._registered = []

    def register(self, cache):
        self._registered.append(cache)

    def display(self, dynamic=False):
        """ Display will print a table of all the caches

        Note : Run this in a new thread if running with dynamic set to True!
        """
        def info_str():
            table = Texttable()
            table.set_cols_align(["l", "l", "r", "r", "l", "l"])
            rows = [c.info() for c in self._registered]
            final = [
                ["Location", "Cache Type", "Entries", "Size (bytes)",
                    "Hit (%)", "Adds causing resize (%)"]] + rows
            table.add_rows(final)
            return table.draw()

        def helper(window):
            window.nodelay(True)
            while (True):
                window.clear()
                window.addstr(info_str())
                window.refresh()
                c = window.getch()
                if c == ord('q'):
                    return
                time.sleep(0.5)

        if dynamic:
            curses.wrapper(helper)
            return

        print(info_str())

GlobalCacheManager = CacheManager()


class Cache(ABC):

    def __init__(self, size, style):
        self._size = size
        self._style = style
        self._max_size = 0
        self._cache = None
        self._hits = 0
        self._misses = 0

    @abstractmethod
    def add(self, key, value):
        raise NotImplementedError("missing implementation")

    @abstractmethod
    def evict(self):
        raise NotImplementedError("missing implementation")

    @abstractmethod
    def bsize(self):
        raise NotImplementedError("missing implementation")

    def fetch(self, key):
        """ Fetches a value from the cache, returns None when key is not there"

        Args:
            key (any): key of value in cache

        Returns:
            returns the value at key in cache, or None if the key does
            not exist.
        """
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        else:
            self._misses += 1
            return None

    def info(self):
        hit_p = 0
        resize_p = 0
        denom = (self._hits + self._misses)
        if denom > 0:
            hit_p = (self._hits / denom) * 100
            resize_p = (self._resizes / self._misses) * 100
        return [self._style, len(self), self.bsize(), hit_p, resize_p]

    def print(self):
        """ Prints all cache entries in the cache"""
        for x, y in self._cache.items():
            print("Key %s : %s" % (str(x), str(y)))

    def __len__(self):

        return len(self._cache)

    def _check_filled(self):
        if self._max_size > 0:
            return self._max_size <= len(self)

        return self.bsize() >= self._size
