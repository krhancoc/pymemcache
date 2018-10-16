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

    def add(self, key, value):
        if self._check_filled():
            self.evict()
        self._cache[key] = value

    def bsize(self):
        sizeof = sys.getsizeof
        size = sizeof(self._hits)
        size += sizeof(self._max_size)
        size += sizeof(self._hits)
        size += sizeof(self._style)
        size += sizeof(self._misses)
        size += sizeof(self._cache)

        return size
