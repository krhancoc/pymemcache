import cache
import logging
import sys

sys.setrecursionlimit(10000)



KB = 1024
MB = 1024 * KB

logging.basicConfig(level=logging.INFO)


@cache.memcache(2 * KB)
def fib(n):
    if n <= 1:

        return n

    return fib(n-1) + fib(n-2)


@cache.memcache(50 * KB)
def fib2(n):
    if n <= 1:

        return n

    return fib2(n-1) + fib2(n-2)


@cache.memcache(2 * KB)
def multiple_param(x, y):
    return x + y

@cache.memcache(2 * KB)
def list_check(y):
    return y

@cache.memcache(2 * KB)
def string_check(y):
    return y

@cache.memcache(2 * KB)
def object_check(y):
    return y

dictionary = {}
for x in range(100000):
    dictionary[x] = x

gcm = cache.GlobalCacheManager
gcm.display()
fib2(1000)
fib2(2000)
multiple_param(1, 2)
multiple_param(1, 2)
list_check([1,2,3,4])
list_check([1,2,3,4])
string_check("hello")
string_check("hello")
object_check(dictionary)
object_check(dictionary)
gcm.display()
