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
        import time
        import threading

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
