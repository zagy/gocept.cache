import unittest
import zope.testing.cleanup


class CleanupTest(zope.testing.cleanup.CleanUp, unittest.TestCase):

    def test_aaa_pollute_cache(self):
        import gocept.cache.method
        gocept.cache.method._caches['foo'] = 'bar'

    def test_caches_should_be_cleared_between_tests(self):
        import gocept.cache.method
        self.assertEqual({}, gocept.cache.method._caches)


class TestCollect(zope.testing.cleanup.CleanUp, unittest.TestCase):

    def test_collect_during_memoize_should_not_prevent_cache(self):
        import gocept.cache.method
        import threading
        import time

        _running = True

        @gocept.cache.method.Memoize(10)
        def takes_a_while():
            while _running:
                time.sleep(0.025)
            return 'value'

        t = threading.Thread(target=takes_a_while)
        t.start()

        gocept.cache.method.collect()
        _running = False
        t.join()
        # caches looks like this:
        # {<function takes_a_while at 0x1013e98c0>:
        #    {((), ()): ('value', 1331375622.015022)}}
        # Assert only that 'value' is there.
        self.assertEqual('value', list(
            list(gocept.cache.method._caches.values())[0].values())[0][0])

    def test_method__collect__1(self):
        """It cleans up caches which timed out."""
        import gocept.cache.method
        import time

        @gocept.cache.method.Memoize(0.2)
        def takes_a_little_while(arg):
            return arg

        takes_a_little_while('one')
        time.sleep(0.1)
        takes_a_little_while('two')
        time.sleep(0.3)
        takes_a_little_while('three')
        func_cache = list(gocept.cache.method._caches.values())[0]
        assert 3 == len(func_cache.values())
        assert sorted([x[0] for x in func_cache.values()]) == [
            'one', 'three', 'two']

        gocept.cache.method.collect()
        func_cache = list(gocept.cache.method._caches.values())[0]
        assert 1 == len(func_cache.values())
        assert 'three' == list(func_cache.values())[0][0]


class TestMemoize(zope.testing.cleanup.CleanUp, unittest.TestCase):
    """Testing ..method.Memoize"""

    def test_method__Memoize__1(self):
        """It applies `ignore_self` only if `self` is the first argument

        in the signature."""
        import gocept.cache.method

        @gocept.cache.method.Memoize(0.1, ignore_self=True)
        def no_self_method(first, second):
            return (first, second)

        @gocept.cache.method.Memoize(0.1, ignore_self=True)
        def self_method(self, second):
            return (self, second)

        no_self_method('one', 'two')
        self_method('three', 'four')
        # We have two different functions with a different length of keys
        cached_keys = [
            list(x.keys())[0][0]
            for x in gocept.cache.method._caches.values()
        ]
        assert [('four',), ('one', 'two')] == sorted(cached_keys)
