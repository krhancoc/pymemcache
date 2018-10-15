import unittest
import random

from cache import LRU, Clock, FIFO


class TestLRU(unittest.TestCase):
    def setUp(self):
        self.lru = LRU(1024)

    def tearDown(self):
        del self.lru

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.lru.add(x, y)
        self.assertTrue(self.lru.bsize() < 1024)

    def check_eviction(self):
        assert False
        for x in range(5):
            y = random.randint(0, 101)
            self.lru.add(x, y)
        key, val = self.lru.evict()
        self.assertTrue(key == 0)
        self.assertTrue(self.lru.fetch(1) is not None)
        key, val = self.lru.evict()
        self.assertTrue(key == 2)

class TestClock(unittest.TestCase):
    def setUp(self):
        self.clock = Clock(1024)

    def tearDown(self):
        del self.clock

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.clock.add(x, y)
        self.assertTrue(self.clock.bsize() < 1024)

    def test_check_eviction(self):
        for x in range(5):
            y = random.randint(0, 101)
            self.clock.add(x, y)
        key, value = self.clock.evict()
        self.assertTrue(key == 0)
        self.assertTrue(self.clock.fetch(1) is not None)
        key, val = self.clock.evict()
        self.assertTrue(key == 2)


class TestFIFO(unittest.TestCase):
    def setUp(self):
        self.fifo = FIFO(1024)

    def tearDown(self):
        del self.fifo

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.fifo.add(x, y)
        self.assertTrue(self.fifo.bsize() < 1024)

    def test_check_eviction(self):
        for x in range(5):
            y = random.randint(0, 101)
            self.fifo.add(x, y)
        key, val = self.fifo.evict()
        self.assertTrue(key == 0)
        self.assertTrue(self.fifo.fetch(1) is not None)
        key, val = self.fifo.evict()
        self.assertTrue(key == 1)
        self.assertTrue(self.fifo.fetch(2) is not None)
        key, val = self.fifo.evict()
        self.assertTrue(key == 2)

    def false(self):
        assert False

if __name__ == '__main__':
    unittest.main()
