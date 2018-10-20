# Cache Algorithms

Example of decorator with the following implementations:

* FIFO (First In First Out)
* LRU (Least Recently Used)
* Clock (Approximation of LRU)
* ARC (Adaptive Replacement Cache)


Demo output:

```
+----------------------------+--------------+---------+--------------+---------+
|          Location          |  Cache Type  | Entries | Size (bytes) | Hit (%) |
+============================+==============+=========+==============+=========+
| decorators.py:fib          | CacheI.FIFO  |    2001 |       170856 | 49.975  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:multiple_par | CacheI.FIFO  |      50 |         8584 | 34.883  |
| am                         |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:list_check   | CacheI.FIFO  |      50 |         8584 | 34.943  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:string_check | CacheI.FIFO  |       1 |          568 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:object_check | CacheI.FIFO  |       1 |          568 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:local_with_s | CacheI.FIFO  |      30 |         4496 | 55.000  |
| ome_random                 |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:fib          | CacheI.LRU   |    2001 |       277360 | 49.975  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:multiple_par | CacheI.LRU   |      50 |         8584 | 34.884  |
| am                         |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:list_check   | CacheI.LRU   |      50 |         8584 | 34.843  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:string_check | CacheI.LRU   |       1 |          568 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:object_check | CacheI.LRU   |       1 |          568 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:local_with_s | CacheI.LRU   |      30 |         4496 | 82.500  |
| ome_random                 |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:fib          | CacheI.ARC   |    2001 |       172616 | 49.975  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:multiple_par | CacheI.ARC   |      48 |        18088 | 34.095  |
| am                         |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:list_check   | CacheI.ARC   |      51 |        18560 | 34.234  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:string_check | CacheI.ARC   |       1 |         2320 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:object_check | CacheI.ARC   |       1 |         2320 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:local_with_s | CacheI.ARC   |      30 |        12984 | 80.742  |
| ome_random                 |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:fib          | CacheI.CLOCK |    2001 |       170856 | 49.975  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:multiple_par | CacheI.CLOCK |      50 |         8584 | 34.527  |
| am                         |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:list_check   | CacheI.CLOCK |      50 |         8584 | 34.875  |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:string_check | CacheI.CLOCK |       1 |          568 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:object_check | CacheI.CLOCK |       1 |          568 | 50      |
+----------------------------+--------------+---------+--------------+---------+
| decorators.py:local_with_s | CacheI.CLOCK |      30 |         4496 | 82.165  |
| ome_random                 |              |         |              |         |
+----------------------------+--------------+---------+--------------+---------+
```

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

# Types include:
# CacheI.FIFO
# CacheI.LRU (DEFAULT)
# CacheI.CLOCK
@memcache(50, CacheI.LRU)
def fib(n):
    if n <= 1:

        return n

    return fib(n-1) + fib(n-2)


```

There exists a GlobalCacheManager object which you can use to monitor your caches, look at demo.py for details


Author: Kenneth Ryan Hancock





