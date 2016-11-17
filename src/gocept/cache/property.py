import transaction
import transaction.interfaces

from zope.interface import implementer


class TransactionJoinError(ValueError):
    """Joining a transaction has failed."""


class TransactionBoundCache(object):

    def __init__(self, name, factory):
        self.attribute = name
        self.factory = factory

    def __get__(self, instance, class_):
        try:
            cache = getattr(instance, self.attribute)
        except AttributeError:
            dm = CacheDataManager(self, instance, transaction.get())
            txn = transaction.get()
            try:
                txn.join(dm)
            except ValueError as e:
                raise TransactionJoinError(str(e))
            cache = self.factory()
            setattr(instance, self.attribute, cache)

        return cache

    def invalidate(self, instance):
        try:
            delattr(instance, self.attribute)
        except AttributeError:
            pass


@implementer(transaction.interfaces.IDataManager)
class CacheDataManager(object):

    def __init__(self, cache, instance, tm):
        self.cache = cache
        self.instance = instance
        self.transaction_manager = tm

    def abort(self, trans):
        self._invalidate()

    def tpc_begin(self, trans):
        pass

    def commit(self, trans):
        pass

    def tpc_vote(self, trans):
        pass

    def tpc_finish(self, trans):
        self._invalidate()

    def tpc_abort(self, trans):
        self._invalidate()

    def sortKey(self):
        return str(id(self))

    def _invalidate(self):
        self.cache.invalidate(self.instance)
