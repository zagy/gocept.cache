# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt

from zope.testing import doctest
import gocept.cache.method
import unittest
import zope.testing.cleanup


class CleanupTest(zope.testing.cleanup.CleanUp, unittest.TestCase):

    def test_aaa_pollute_cache(self):
        gocept.cache.method._caches['foo'] = 'bar'

    def test_caches_should_be_cleared_between_tests(self):
        self.assertEqual({}, gocept.cache.method._caches)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CleanupTest))
    suite.addTest(doctest.DocFileSuite(
        'README.txt',
        optionflags=doctest.ELLIPSIS))
    return suite
