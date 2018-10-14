import cache
import logging

logging.basicConfig(level=logging.DEBUG)

lru = cache.LRU(2048)

for x in range(15):
    lru.add(x, 10)


assert lru.fetch("not_in_here") is None
assert 10 == lru.fetch(0)
key, val = lru.pop()
assert key == 1
assert 10 == lru.fetch(2)
key, val = lru.pop()
assert key == 3


@cache.memcache(2048)
def fib(n):
    if n <= 1:

        return n

    return fib(n-1) + fib(n-2)


@cache.memcache(10000)
def fib2(n):
    if n <= 1:

        return n

    return fib2(n-1) + fib2(n-2)


gcm = cache.GlobalCacheManager
gcm.display()
fib2(110)
gcm.display()
