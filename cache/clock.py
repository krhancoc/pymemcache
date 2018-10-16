import sys

from itertools import cycle
from collections import OrderedDict
from .cache import Cache, CacheI



class Clock(Cache):
    """ Clock is an approximation of LRU
    
    Clock works by having a circlar style structure, and a second chance
    mechanism.  The clock pointer points at some index in the cache, 
    when an eviction is needed, it look at the head, checks the element there
    if the bit set is 1, set it to 0 and move the next element, if its 0, then evict
    that element

    """
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
                self._clock_head += 1
                self._clock_head = self._clock_head % len(self._cache)
                return (key, self._cache.pop(key)[0])
            else:
                val[1] = 0
            self._clock_head += 1
            self._clock_head = self._clock_head % len(self._cache)

    def add(self, key, value):
        if self._check_filled():
            self.evict()
        self._cache[key] = [value, 1]

    def fetch(self, key):
        val = super().fetch(key)
        if val is not None:
            val[1] = 1
            return val[0]

        return None

    def bsize(self):
        sizeof = sys.getsizeof
        size = sizeof(self._hits)
        size += sizeof(self._max_size)
        size += sizeof(self._hits)
        size += sizeof(self._style)
        size += sizeof(self._misses)
        size += sizeof(self._cache)

        return size
