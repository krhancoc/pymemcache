# Cache Algorithms

Example of decorator with the following implementations:

* FIFO (First In First Out)
* LRU (Least Recently Used)
* Clock (Approximation of LRU)

This is to accompany a blog post.


## Startup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python tests.py
```


## Demo

```bash
python demo.py
```

Pressing 'q' exists the dynamic view of the demo

## Usage



```python
from cache import memcache, CacheI

KB = 1024
# Types include:
# CacheI.FIFO
# CacheI.LRU (DEFAULT)
# CacheI.CLOCK
# Minimum size of 2 Kilobytes
@memcache(2 * KB, CacheI.LRU)
def fib(n):
    if n <= 1:

        return n

    return fib(n-1) + fib(n-2)


```

There exists a GlobalCacheManager object which you can use to monitor your caches, look at demo.py for details


Author: Kenneth Ryan Hancock





