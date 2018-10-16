from cache import memcache, GlobalCacheManager, CacheI
from threading import Thread
import logging
import sys
import random

sys.setrecursionlimit(10000)


KB = 1024
MB = 1024 * KB

logging.basicConfig(level=logging.INFO)

def cache_test(t):

    @memcache(5000, t)
    def fib(n):
        if n <= 1:

            return n

        return fib(n-1) + fib(n-2)


    @memcache(50, t)
    def multiple_param(x, y):
        return x + y


    @memcache(50, t)
    def list_check(y):
        return y


    @memcache(30, t)
    def string_check(y):
        return y


    @memcache(30, t)
    def object_check(y):
        return y

    @memcache(30, t)
    def local_with_some_random(y):
        return y


    dictionary = {}
    for x in range(100000):
        dictionary[x] = x

    fib(1000)
    fib(2000)
    for x in range(100, 100000, 1000):
        for _ in range(100):

            #localized
            for t in range(x - 10, x + 10):
                t = int(t)
                local_with_some_random(t)

            #random
            for _ in range(4):
                r = random.randint(1000000, 2000000)
                local_with_some_random(r)

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
#t = Thread(target = gcm.display, args = (True,))
#t.start()
#cache_test(CacheI.FIFO)
#cache_test(CacheI.LRU)
cache_test(CacheI.ARC)
#cache_test(CacheI.CLOCK)
#t.join()
gcm.display()
