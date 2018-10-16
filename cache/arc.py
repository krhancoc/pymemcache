# -*- coding: utf-8 -*-
# Author : Kenneth Ryan Hancock

import sys
from collections import OrderedDict

from .cache import Cache, CacheI
from .fifo import FIFO
from .lru import LRU


class ARC(Cache):
    """ ARC - Adapative replacement cache implementation

    ARC's implementation is a combination of 4 seperate caches,
    T1, T2, B1, B2, where T1 and T2 will hold actual data, and B1, B2
    will hold ghost entries.  T1 and T2 both start at size/2 .

    The T1, is a standard FIFO cache, that when a hit occurs will be deleted
    from the cache and upgraded to the T2 cache, if no hit occurs it will
    be moved up the queue and evicted.  Evicted T1 entries are placed into the 
    B1 cache but with no data (just the key), which are a standard FIFO queue 
    as well.

    T2, is a frequently used cache but in reality is also just an LRU cache.
    When hits occur in the T2 cache, they follow the same procedure as an LRU.  
    When T2 entries are evicted they are placed within the B2 cache with no 
    data.
    
    B1 is the T1 ghost entrie cache, when a hit occurs in this cache in means
    that the T1 cache should be expanded and the T2 shrunk, a standard miss occurs,
    but max sizes of each cache are adjusted.

    B2 is for T2 that B1 is for T1.

    Args:
        size (int) : max number of entries in the cache
    """
    def __init__(self, size):

        super().__init__(size, CacheI.ARC)
        self._t1 = FIFO(int(size / 2))
        self._t2 = LRU(int(size / 2))
        self._b1 = FIFO(int(size / 2))
        self._b2 = FIFO(int(size / 2))
        self._boundary = int(size / 2)

    def fetch(self, key):

        # Hit in T1 -- Upgrade to T2
        val = self._t1.fetch(key)
        if val is not None:
            self._t1.delete(key)
            if self._t2._check_filled():
                k, _ = self._t2.evict()
                self._b2.add(k, '')
            self._t2.add(key, val)
            self._hits += 1
            return val

        # Hit in B1 -- Allocate more space for T1
        val = self._b1.fetch(key)
        if val is not None:
            if (self._t2._max_size > 1):
                self._t1._max_size += 1
                self._t2._max_size -= 1
            self._misses += 1
            return None

        # Hit in T2 -- Standard LRU hit
        val = self._t2.fetch(key)
        if val is not None:
            self._hits += 1
            return val

        # Hit in B2 -- Allocate more space for T2
        val = self._b2.fetch(key)
        if val is not None:
            if (self._t1._max_size > 1):
                self._t1._max_size -= 1
                self._t2._max_size += 1
            self._misses += 1
            return None

        self._misses += 1
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
