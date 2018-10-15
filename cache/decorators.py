import os
import pickle

from .cache import CacheI, GlobalCacheManager
from .lru import LRU
from .clock import Clock
from .fifo import FIFO


def memcache(size, style=CacheI.LRU):
    """Decorator caching object for functions"""
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
                self.cache = Clock(size)
            elif val == CacheI.FIFO:
                self.cache = FIFO(size)

        def info(self):
            info = []
            info.append(
                "%s:%s" %
                (os.path.basename(__file__),
                 self.func.__name__))
            info.extend(self.cache.info())

            return info

    return cacheobject
