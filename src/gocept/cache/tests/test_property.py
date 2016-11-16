import transaction
from gocept.cache.property import TransactionBoundCache

try:
    import unittest.mock as mock
except ImportError:
    import mock


class Foo(object):
    cache = TransactionBoundCache('_v_cache', dict)


def test_property__TransactionBoundCache__invalidate__1():
    """It can be called twice."""
    foo = Foo()
    foo.cache['A'] = 1
    # TransactionBoundCache is a descriptor, so we have to fetch it from the
    # data manager:
    transaction.get()._resources[0].cache.invalidate(foo)
    transaction.get()._resources[0].cache.invalidate(foo)


class VoteExceptionDataManager(object):
    """DataManager which raises an exception in tpc_vote."""

    def abort(self, trans):
        pass

    def commit(self, trans):
        pass

    def tpc_begin(self, trans):
        pass

    def tpc_vote(self, trans):
        raise RuntimeError()

    def tpc_abort(self, trans):
        pass

    def sortKey(self):
        # Make sure CacheDataManager.abort() is not called by making sure we
        # vote last:
        return '~sort-me-last'


def test_property__CacheDataManager__tpc_abort__1():
    """It invalidates the cache."""
    foo = Foo()
    foo.cache['A'] = 1
    # tpc_abort is called on commit if a data manager raises an exception in
    # tpc_vote:
    transaction.get().join(VoteExceptionDataManager())
    try:
        transaction.commit()
    except RuntimeError:
        pass
    # We cannot join a transaction in status COMMITFAILED:
    with mock.patch('transaction._transaction.Transaction.join'):
        assert {} == foo.cache
