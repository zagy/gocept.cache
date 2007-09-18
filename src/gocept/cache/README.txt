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


The same happens on abort -- once we get a ZODB supporting it:

#>>> foo.cache['A'] = 1
#>>> foo.cache
#{'A': 1}
#>>> transaction.abort()
#>>> foo.cache
#{}

