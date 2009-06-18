============
gocept.cache
============

Method cache
============

Memoize with timeout
--------------------

Memoize with timeout caches methods with a certain timeout:

>>> import math
>>> import gocept.cache.method
>>>
>>> class Point(object):
...
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...
...     @gocept.cache.method.Memoize(0.1)
...     def distance(self, x, y):
...         print 'computing distance'
...         return math.sqrt((self.x - x)**2 + (self.y - y)**2)
...
...     @gocept.cache.method.Memoize(0.1, ignore_self=True)
...     def add_one(self, i):
...         if not isinstance(i, int):
...             print "I want an int"
...         else:
...             print 'adding one'
...             return i + 1
...
>>> point = Point(1.0, 2.0)

When we first ask for the distance it is computed:

>>> point.distance(2, 2)
computing distance
1.0

The second time the distance is not computed but returned from the cache:

>>> point.distance(2, 2)
1.0

Now, let's wait 0.1 secondes, the value we set as cache timeout. After that the
distance is computed again:

>>> import time
>>> time.sleep(0.5)
>>> point.distance(2, 2)
computing distance
1.0


When we create a new instance, the new instance gets its own cache:

>>> p2 = Point(1.0, 2.0)
>>> p2.distance(2, 2)
computing distance
1.0

It's also possible to explicitly ignore self. We did this for the `add_one`
method:

>>> point.add_one(3)
adding one
4

The second time it's not computed as you would expect:
>>> point.add_one(3)
4

If we ask `p2` now the result is not computed as well:

>>> p2.add_one(3)
4

If we put a non hashable argument into a memoized function it will not be
cached:

>>> point.add_one({'a': 1})
I want an int
>>> point.add_one({'a': 1})
I want an int


The decorated method can be introspected and yields the same results ad the
original:

>>> import inspect
>>> Point.distance.func_name
'distance'
>>> inspect.getargspec(Point.distance)
(['self', 'x', 'y'], None, None, None)

Store memoizations on an attribute
----------------------------------

If you want more control over the cache used by gocept.cache.method.Memoize
(e. g. you want to associate it with a gocept.cache.property.CacheDataManager
to invalidate it on transaction boundaries), you can use the @memoize_on_attribute
decorator to retrieve the cache-dictionary from the instance:

>>> class Bar(object):
...     cache = {}
...
...     @gocept.cache.method.memoize_on_attribute('cache', 10)
...     def echo(self, x):
...         print 'miss'
...         return x

>>> bar = Bar()
>>> bar.echo(5)
miss
5
>>> bar.echo(5)
5
>>> bar.cache.clear()
>>> bar.echo(5)
miss
5

This decorator should be used on methods, not on plain functions, since it must
be able to retrieve the cache-dictionary from the first argument of the function
(which is 'self' for methods):

>>> @gocept.cache.method.memoize_on_attribute('cache', 10)
... def bar():
...     print 'foo'
>>> bar()
Traceback (most recent call last):
TypeError: gocept.cache.method.memoize_on_attribute could not retrieve cache attribute 'cache' for function <function bar at 0x...>

>>> @gocept.cache.method.memoize_on_attribute('cache', 10)
... def baz(x):
...     print 'foo'
>>> baz(5)
Traceback (most recent call last):
TypeError: gocept.cache.method.memoize_on_attribute could not retrieve cache attribute 'cache' for function <function baz at 0x...>


Cached Properties
=================

Transaction Bound Cache
-----------------------

The transaction bound cache is invalidated on transaction boundaries.

Create a class and set some data:

>>> import gocept.cache.property
>>> class Foo(object):
...
...     cache = gocept.cache.property.TransactionBoundCache('_cache', dict)
...
>>> foo = Foo()
>>> foo.cache
{}
>>> foo.cache['A'] = 1
>>> foo.cache
{'A': 1}

If we commit the transaction the cache is empty again:

>>> import transaction
>>> transaction.commit()
>>> foo.cache
{}


The same happens on abort:

>>> foo.cache['A'] = 1
>>> foo.cache
{'A': 1}
>>> transaction.abort()
>>> foo.cache
{}
