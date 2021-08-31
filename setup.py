from setuptools import find_packages
from setuptools import setup
import os.path


tests_require = []


setup(
    name='gocept.cache',
    version='5.0',
    author="gocept",
    author_email="mail@gocept.com",
    description="Cache descriptors for Python and Zope",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords='cache transaction bound zope',
    long_description=(
        ".. contents::\n\n" +
        open(os.path.join('src', 'gocept', 'cache', 'README.rst')).read() +
        '\n\n' +
        open('CHANGES.rst').read()),
    license="MIT",
    url='https://github.com/gocept/gocept.cache',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    include_package_data=True,
    zip_safe=False,

    namespace_packages=['gocept'],
    python_requires='>=3.7, <4',
    install_requires=[
        'decorator',
        'setuptools',
        'transaction',
        'zope.testing',
    ],
    extras_require=dict(
        test=tests_require),
)
