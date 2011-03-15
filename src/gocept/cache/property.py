# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt

import transaction
import transaction.interfaces

import zope.interface


class TransactionBoundCache(object):

    def __init__(self, name, factory):
        self.attribute = name
        self.factory = factory

    def __get__(self, instance, class_):
        try:
            cache = getattr(instance, self.attribute)
        except AttributeError:
            cache = self.factory()
            setattr(instance, self.attribute, cache)
            dm = CacheDataManager(self, instance, transaction.get())
            transaction.get().join(dm)

        return cache

    def invalidate(self, instance):
        try:
            delattr(instance, self.attribute)
        except AttributeError:
            pass


class CacheDataManager(object):

    zope.interface.implements(transaction.interfaces.IDataManager)

    def __init__(self, cache, instance, tm):
        self.cache = cache
        self.instance = instance
        self.transaction_manager = tm

    def abort(self, trans):
        self._invalidate()

    def tpc_begin(self, trans):
        pass

    def commit(self, trans):
        self._invalidate()

    def tpc_vote(self, trans):
        self._invalidate()

    def tpc_finish(self, trans):
        pass

    def tpc_abort(self, trans):
        self._invalidate()

    def sortKey(self):
        return str(id(self))

    def _invalidate(self):
        self.cache.invalidate(self.instance)
