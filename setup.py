# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt

import os.path

from setuptools import setup, find_packages


setup(
    name = 'gocept.cache',
    version='0.6.2.dev0',
    author = "Christian Zagrodnick",
    author_email = "cz@gocept.com",
    description = "Cache descriptors for Python and Zope",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
    ],
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
