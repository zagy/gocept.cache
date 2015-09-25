import os.path
from setuptools import setup, find_packages


setup(
    name='gocept.cache',
    version='1.0',
    author="gocept",
    author_email="mail@gocept.com",
    description="Cache descriptors for Python and Zope",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: Zope Public License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    long_description=(
        ".. contents::\n\n" +
        open(os.path.join(os.path.dirname(__file__),
                          'src', 'gocept', 'cache', 'README.txt')).read() +
        '\n\n' +
        open(os.path.join(os.path.dirname(__file__), 'CHANGES.txt')).read()),
    license="ZPL 2.1",
    url='https://bitbucket.org/gocept/gocept.cache',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    include_package_data=True,
    zip_safe=False,

    namespace_packages=['gocept'],
    install_requires=[
        'decorator',
        'setuptools',
        'transaction',
        'zope.testing',
    ],
)
