from cache import memcache, GlobalCacheManager, CacheI
from threading import Thread
import logging
import sys
import random

sys.setrecursionlimit(10000)


KB = 1024
MB = 1024 * KB

logging.basicConfig(level=logging.INFO)

@memcache(5 * KB, CacheI.CLOCK)
def fib2(n):
    if n <= 1:

        return n

    return fib2(n-1) + fib2(n-2)


def cache_test(t):

    @memcache(2 * KB, t)
    def fib(n):
        if n <= 1:

            return n

        return fib(n-1) + fib(n-2)


    @memcache(50 * KB, t)
    def fib2(n):
        if n <= 1:

            return n

        return fib2(n-1) + fib2(n-2)


    @memcache(2 * KB, t)
    def multiple_param(x, y):
        return x + y


    @memcache(2 * KB, t)
    def list_check(y):
        return y


    @memcache(2 * KB, t)
    def string_check(y):
        return y


    @memcache(2 * KB, t)
    def object_check(y):
        return y


    dictionary = {}
    for x in range(100000):
        dictionary[x] = x

    fib2(1000)
    fib2(2000)
    for x in range(10000):
        fib(500)

    for x in range(100000):
        k = random.randint(0, 11)
        j = random.randint(0, 11)
        multiple_param(k, j)

    for x in range(100000):
        l = [random.randint(0, 11), random.randint(0, 11)]
        list_check(l)

    string_check("hello")
    string_check("hello")
    object_check(dictionary)
    object_check(dictionary)

gcm = GlobalCacheManager
t = Thread(target = gcm.display, args = (True,))
t.start()

for x in range(3000):
    fib2(x)
cache_test(CacheI.LRU)
cache_test(CacheI.CLOCK)
cache_test(CacheI.FIFO)
t.join()
gcm.display()
