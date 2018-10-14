import sys

from itertools import cycle
from collections import OrderedDict
from .cache import Cache, CacheI



class Clock(Cache):

    def __init__(self, size):
        super().__init__(size, CacheI.CLOCK)
        self._cache = OrderedDict()
        self._clock_head = 0
        self._resizes = 0


    def evict(self):
        items = list(self._cache.items())
        while (True):
            key, val = items[self._clock_head]
            if val[1] == 0:
                self._cache.pop(key)
                break
            else:
                val[1] = 0
            self._clock_head += 1
            if self._max_size == 0:
                self._clock_head = self._clock_head % self._max_size
            else:
                self._clock_head = self._clock_head % len(self._cache)


    def add(self, key, value):
        if self._check_filled():
            self.evict()
        self._cache[key] = [value, 1]
        if (self.bsize() > self._size):
            self.resize(key)
            self.add(key, value)

    def resize(self, exclude):
        self._resizes += 1
        self._max_size = len(self._cache) - 2
        new_cache = OrderedDict()
        for k, val in self._cache.items():
            if k != exclude:
                new_cache[k] = val
        self._cache = new_cache

    def fetch(self, key):
        if key in self._cache:
            self._hits += 1
            return self._cache[key][0]
        else:
            self._misses += 1
            return None


    def bsize(self):
        sizeof = sys.getsizeof
        size = sizeof(self._hits)
        size += sizeof(self._size)
        size += sizeof(self._hits)
        size += sizeof(self._style)
        size += sizeof(self._misses)
        size += sizeof(self._cache)

        return size
