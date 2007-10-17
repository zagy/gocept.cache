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


The same happens on abort -- once we get a ZODB supporting it::

#>>> foo.cache['A'] = 1
#>>> foo.cache
#{'A': 1}
#>>> transaction.abort()
#>>> foo.cache
#{}

