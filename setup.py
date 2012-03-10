# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt

import os.path

from setuptools import setup, find_packages


setup(
    name = 'gocept.cache',
    version='0.5.1',
    author = "Christian Zagrodnick",
    author_email = "cz@gocept.com",
    description = "Cache descriptors for Python and Zope",
    long_description = (
        open(os.path.join(os.path.dirname(__file__),
                          'src', 'gocept', 'cache', 'README.txt')).read() +
        '\n\n' +
        open(os.path.join(os.path.dirname(__file__), 'CHANGES.txt')).read()),
    license = "ZPL 2.1",
    url='http://pypi.python.org/pypi/gocept.cache',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    include_package_data = True,
    zip_safe = False,

    namespace_packages = ['gocept'],
    install_requires = [
        'decorator',
        'setuptools',
        'transaction',
        'zope.testing',
    ],
)
