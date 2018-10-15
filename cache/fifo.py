import sys
from collections import OrderedDict

from .cache import Cache, CacheI

class FIFO(Cache):

    def __init__(self, size):
        super().__init__(size, CacheI.FIFO)
        self._cache = OrderedDict()
        self._clock_head = 0
        self._resizes = 0

    def evict(self):
        return self._cache.popitem(last=False)

    def resize(self, exclude):
        self._resizes += 1
        self._max_size = len(self._cache) - 2
        new_cache = OrderedDict()
        for k, val in self._cache.items():
            if k != exclude:
                new_cache[k] = val
        self._cache = new_cache

    def add(self, key, value):
        if self._check_filled():
            self.evict()
        self._cache[key] = value
        if (self.bsize() > self._size):
            self.resize(key)
            self.add(key, value)

    def bsize(self):
        sizeof = sys.getsizeof
        size = sizeof(self._hits)
        size += sizeof(self._size)
        size += sizeof(self._hits)
        size += sizeof(self._style)
        size += sizeof(self._misses)
        size += sizeof(self._cache)

        return size
