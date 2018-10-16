import unittest
import random

from cache import LRU, Clock, FIFO, ARC


class TestLRU(unittest.TestCase):
    def setUp(self):
        self.lru = LRU(50)

    def tearDown(self):
        del self.lru

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.lru.add(x, y)
        self.assertTrue(len(self.lru) <= 50 )

    def test_check_eviction(self):
        for x in range(5):
            y = random.randint(0, 101)
            self.lru.add(x, y)
        key, val = self.lru.evict()
        self.assertTrue(key == 0)
        self.assertTrue(self.lru.fetch(1) is not None)
        self.assertTrue(self.lru.fetch(2) is not None)
        self.assertTrue(self.lru.fetch(4) is not None)
        key, val = self.lru.evict()
        self.assertTrue(key == 3)

class TestClock(unittest.TestCase):
    def setUp(self):
        self.clock = Clock(50)

    def tearDown(self):
        del self.clock

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.clock.add(x, y)
        self.assertTrue(len(self.clock) <= 50)

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
        self.fifo = FIFO(50)

    def tearDown(self):
        del self.fifo

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.fifo.add(x, y)
        self.assertTrue(len(self.fifo) <= 50)

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

class TestARC(unittest.TestCase):
    def setUp(self):
        self.arc = ARC(60)

    def tearDown(self):
        del self.arc

    def test_max_size(self):
        for x in range(100000):
            y = random.randint(0, 101)
            self.arc.add(x, y)
        self.assertTrue(len(self.arc) <= 60)

    def test_check_eviction(self):
        for x in range(60):
            y = random.randint(0, 101)
            self.arc.add(x, y)
        for x in range(30):
            val = self.arc.fetch(x)
        for x in range(61, 92):
            y = random.randint(0, 101)
            self.arc.add(x, y)
        self.arc.fetch(32)
        self.arc.fetch(33)
        self.arc.print()
        print(len(self.arc))
        #  self.assertTrue(val != None)
        #  self.assertTrue(len(self.arc) == 30)
        #  for x in range(10, 20):
            #  val = self.arc.fetch(x)
        #  self.assertTrue(len(self.arc) == 30)
        #  for x in range(50, 100):
            #  y = random.randint(0, 101)
            #  self.arc.add(x, y)
        #  self.arc.print()
        #  print(len(self.arc))
        #  for x in range(20, 60):
            #  self.arc.fetch(x)


if __name__ == '__main__':
    unittest.main()

