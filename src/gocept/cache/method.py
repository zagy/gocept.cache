# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt

import decorator
import inspect
import time
import zope.testing.cleanup


_caches = {}
_timeouts = {}


def collect():
    """Clear cache of results which have timed out"""
    for func in _caches:
        for key in list(_caches[func]):
            if (time.time() - _caches[func][key][1] >=
                _timeouts[func]):
                _caches[func].pop(key, None)


def clear():
    _caches.clear()
    _timeouts.clear()


zope.testing.cleanup.addCleanUp(clear)


def Memoize(timeout, ignore_self=False, _caches=_caches, _timeouts=_timeouts):
    """Memoize With Timeout

    Based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/325905

    """

    @decorator.decorator
    def func(f, *args, **kwargs):
        cache = _caches.setdefault(f, {})
        _timeouts.setdefault(f, timeout)

        cache_args = args
        if ignore_self:
            arguments = inspect.getargspec(f)[0]
            if arguments and arguments[0] == 'self':
                cache_args = args[1:]

        kw = kwargs.items()
        kw.sort()
        key = (cache_args, tuple(kw))

        try:
            hash(key)
        except TypeError:
            # Not hashable.
            key = None

        try:
            value, cached_time = cache[key]
            #print "cache"
            if (time.time() - cached_time) > timeout:
                raise KeyError
        except KeyError:
            #print "new"
            value = f(*args,**kwargs)
            if key is not None:
                cache[key] = (value, time.time())
        return value

    return func


def memoize_on_attribute(attribute_name, timeout, ignore_self=False):
    @decorator.decorator
    def func(function, *args, **kw):
        try:
            self = args[0]
            cache = getattr(self, attribute_name)
        except (IndexError, AttributeError):
            raise TypeError(
                "gocept.cache.method.memoize_on_attribute could"
                + " not retrieve cache attribute '%s' for function %r"
                % (attribute_name, function))
        return Memoize(timeout, _caches=cache,
                       ignore_self=ignore_self)(function)(*args, **kw)
    return func
