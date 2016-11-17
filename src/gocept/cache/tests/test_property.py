import pytest
import transaction
from gocept.cache.property import TransactionBoundCache, TransactionJoinError

try:
    import unittest.mock as mock
except ImportError:
    import mock


class Foo(object):
    """Example object having a TransactionBoundCache."""

    cache = TransactionBoundCache('_v_cache', dict)


def test_property__TransactionBoundCache__invalidate__1():
    """It can be called twice."""
    foo = Foo()
    foo.cache['A'] = 1
    # TransactionBoundCache is a descriptor, so we have to fetch it from the
    # data manager:
    transaction.get()._resources[0].cache.invalidate(foo)
    transaction.get()._resources[0].cache.invalidate(foo)


class NoopDatamanager(object):
    """Datamanager which does nothing."""

    def abort(self, trans):
        pass

    def commit(self, trans):
        pass

    def tpc_begin(self, trans):
        pass

    def tpc_abort(self, trans):
        pass


class VoteExceptionDataManager(NoopDatamanager):
    """DataManager which raises an exception in tpc_vote."""

    def tpc_vote(self, trans):
        raise RuntimeError()

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


class JoiningTransactionBoundCacheDuringCommitDataManager(NoopDatamanager):
    """Datamanager which accesses a TransactionBoundCache during commit."""

    def __init__(self, obj, cache_attr):
        self.obj = obj
        self.cache_attr = cache_attr

    def commit(self, trans):
        getattr(self.obj, self.cache_attr)


def test_property__TransactionBoundCache____get____1():
    """It raises a TransactionJoinError if called first time during commit."""
    foo = Foo()
    dm = JoiningTransactionBoundCacheDuringCommitDataManager(foo, 'cache')
    txn = transaction.begin()
    txn.join(dm)
    with pytest.raises(TransactionJoinError) as err:
        transaction.commit()
    assert (
        "expected txn status 'Active' or 'Doomed', but it's 'Committing'" ==
        str(err.value))
