=======
Changes
=======

2.1 (2016-11-17)
================

- Bugfix: ``.property.CacheDataManager`` no longer invalidates the cache in
  ``tpc_vote()`` and ``commit()`` but in ``tpc_finish()``.

- Raise `TransactionJoinError` if joining the transaction failed in
  ``.property.TransactionBoundCache``.


2.0 (2016-03-18)
================

- Drop support of Python 2.6.

- Declare support of PyPy and PyPy3.


1.0 (2015-09-25)
================

- Now testing against currently newest versions of dependencies.

- Drop support of Python 3.2.

- Declare Support of Python 3.4 and 3.5.


0.6.1 (2013-09-13)
==================

- Finish Python 3 compatibility


0.6 (2013-09-13)
================

- Changes not recored, sorry.


0.6b2 (2013-09-05)
==================

- Changes not recored, sorry.


0.6b1 (2013-09-05)
==================

- Python3 compatibility


0.5.2 (2012-06-22)
==================

- Added ``gocept.cache.method.do_not_cache_and_return(value)`` in memoized
  methods/functions which will return the given value, without caching it.

0.5.1 (2012-03-10)
==================

- Prevent race condition which caused values of ``gocept.cache.method.Memoize``
  not to be stored when collect was called during the Memoize call
  (in multi threaded environments).

- Pin test versions to ZTK 1.1

0.5 (2011-03-15)
================

- Replace dependency on ZODB with a dependency on transaction.

0.4 (2009-06-18)
================

- Registered clearing the cache with zope.testing.cleanup.

0.3 (2008-12-19)
================

- Added @memoize_on_attribute to retrieve the memoization cache from the
  instance instead of using gocept.cache.method's built-in cache.

0.2.2 (2007-12-17)
==================

- Fixed the bug in `TransactionBoundCache` where the cache was not invalidated
  on transaction abort.

0.2.1 (2007-10-17)
==================

- Fixed a bug in `TransactionBoundCache` which yielded an error in the log:
  `TypeError: <lambda>() takes exactly 1 argument (2 given)`
