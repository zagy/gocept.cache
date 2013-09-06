import doctest


def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        package='gocept.cache',
        optionflags=doctest.ELLIPSIS)
