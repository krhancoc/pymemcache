import sys
from collections import OrderedDict

from .cache import Cache, CacheI
from .fifo import FIFO
from .lru import LRU


class ARC(Cache):

    def __init__(self, size):

        super().__init__(size, CacheI.ARC)
        self._t1 = FIFO(int(size / 2))
        self._t2 = LRU(int(size / 2))
        self._b1 = FIFO(int(size / 2))
        self._b2 = FIFO(int(size / 2))
        self._boundary = int(size / 2)
        self._resizes = 0

    @property
    def misses(self):

        return self._misses

    @misses.setter
    def misses(self, val):
        
        if self._t1._max_size > self._boundary:
            self._t1._max_size -= 1
            self._t2._max_size += 1
        elif self._t1._max_size < self._boundary:
            self._t1._max_size += 1
            self._t2._max_size -= 1
        
        self._misses = val

    def fetch(self, key):
        val = self._t1.fetch(key)
        if val is not None:
            self._t1.delete(key)
            if self._t2._check_filled():
                k, _ = self._t2.evict()
                self._b2.add(k, '')
            self._t2.add(key, val)
            self._hits += 1
            return val

        val = self._b1.fetch(key)
        if val is not None:
            if (self._t2._max_size > 1):
                self._t1._max_size += 1
                self._t2._max_size -= 1
            return None

        val = self._t2.fetch(key)
        if val is not None:
            self._hits += 1
            return val

        val = self._b2.fetch(key)
        if val is not None:
            if (self._t1._max_size > 1):
                self._t1._max_size -= 1
                self._t2._max_size += 1
            return None

        self.misses += 1
        return val

    def evict(self):
        key, val = self._t1.evict()
        self._b1.add(key, '')
        return (key, val)
            
    def print(self):
        print("==== T1 ====")
        self._t1.print()
        print("==== T2 ====")
        self._t2.print()
        print("==== B1 ====")
        self._b1.print()
        print("==== B2 ====")
        self._b2.print()

    def __len__(self):

        return len(self._t1) + len(self._t2)


    def add(self, key, value):
        if self._t1._check_filled():
            self.evict()
        self._t1.add(key, value)
        if self._b1.fetch(key) is not None:
            self._b1.delete(key)

    def bsize(self):
        sizeof = sys.getsizeof
        size = sizeof(self._hits)
        size += sizeof(self._max_size)
        size += sizeof(self._hits)
        size += sizeof(self._style)
        size += sizeof(self._misses)
        size += self._t1.bsize()
        size += self._t2.bsize()
        size += self._b1.bsize()
        size += self._b2.bsize()

        return size
