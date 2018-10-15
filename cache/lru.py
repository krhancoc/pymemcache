import sys
from collections import OrderedDict

from .cache import Cache, CacheI


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
        self._cache = OrderedDict()
        self._max_size = -1
        self._resizes = 0

    # @profile
    def evict(self):
        """ Pops the least recently used element from the cache"""
        return self._cache.popitem(last=False)

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
            self.evict()
        self._cache[key] = value
        if (self.bsize() > self._size):
            self.resize(key)
            self.add(key, value)

    def fetch(self, key):
        result = super().fetch(key)
        if result is not None:
            val = self._cache.pop(key)
            self.add(key, val)

        return result

    def resize(self, exclude):
        self._resizes += 1
        self._max_size = len(self._cache) - 2
        new_cache = OrderedDict()
        for k, val in self._cache.items():
            if k != exclude:
                new_cache[k] = val
        self._cache = new_cache

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

    def __str__(self):
        hit_p = 0
        resize_p = 0
        denom = (self._hits + self._misses)
        if denom > 0:
            hit_p = (self._hits / denom) * 100
            resize_p = (self._resizes / self._misses) * 100
        return "%s - %d entries, %d bytes, %.2f%% hit, %.2f%% adds cause resize" % \
            (self._style, len(self), self.bsize(), hit_p, resize_p)
