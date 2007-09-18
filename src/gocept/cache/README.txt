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
