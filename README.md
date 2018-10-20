# Cache Algorithms

Example of decorator with the following implementations:

* FIFO (First In First Out)
* LRU (Least Recently Used)
* Clock (Approximation of LRU)
* ARC (Adaptive Replacement Cache)


Demo output:

+--------------+--------------+---------+--------------+---------+-------------+
|   Location   |  Cache Type  | Entries | Size (bytes) | Hit (%) |    Adds     |
|              |              |         |              |         |   causing   |
|              |              |         |              |         | resize (%)  |
+==============+==============+=========+==============+=========+=============+
| decorators.p | CacheI.LRU   |     430 |        40740 | 49.975  | 0.650       |
| y:fib        |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.LRU   |       8 |         1420 | 5.572   | 0.008       |
| y:multiple_p |              |         |              |         |             |
| aram         |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.LRU   |       8 |         1420 | 5.550   | 0.008       |
| y:list_check |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.LRU   |       1 |          592 | 50      | 0           |
| y:string_che |              |         |              |         |             |
| ck           |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.LRU   |       1 |          592 | 50      | 0           |
| y:object_che |              |         |              |         |             |
| ck           |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.LRU   |      32 |         4588 | 82.500  | 0.005       |
| y:local_with |              |         |              |         |             |
| _some_random |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.CLOCK |     631 |        47144 | 49.975  | 2.599       |
| y:fib        |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.CLOCK |       9 |         1424 | 6.293   | 0.014       |
| y:multiple_p |              |         |              |         |             |
| aram         |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.CLOCK |       9 |         1424 | 6.205   | 0.014       |
| y:list_check |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.CLOCK |       1 |          568 | 50      | 0           |
| y:string_che |              |         |              |         |             |
| ck           |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.CLOCK |       1 |          568 | 50      | 0           |
| y:object_che |              |         |              |         |             |
| ck           |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.CLOCK |      33 |         4592 | 81.663  | 0.039       |
| y:local_with |              |         |              |         |             |
| _some_random |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.FIFO  |     631 |        47144 | 49.975  | 2.599       |
| y:fib        |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.FIFO  |       9 |         1424 | 6.165   | 0.014       |
| y:multiple_p |              |         |              |         |             |
| aram         |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.FIFO  |       9 |         1424 | 6.280   | 0.014       |
| y:list_check |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.FIFO  |       1 |          568 | 50      | 0           |
| y:string_che |              |         |              |         |             |
| ck           |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.FIFO  |       1 |          568 | 50      | 0           |
| y:object_che |              |         |              |         |             |
| ck           |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+
| decorators.p | CacheI.FIFO  |      33 |         4592 | 62.559  | 0.019       |
| y:local_with |              |         |              |         |             |
| _some_random |              |         |              |         |             |
+--------------+--------------+---------+--------------+---------+-------------+


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





