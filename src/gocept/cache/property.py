# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import transaction


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
            transaction.get().addBeforeCommitHook(
                self.invalidate, (instance, ))
            transaction.get().addAfterCommitHook(
                lambda commit_or_abort: self.invalidate(instance))
        return cache

    def invalidate(self, instance):
        try:
            delattr(instance, self.attribute)
        except AttributeError:
            pass
