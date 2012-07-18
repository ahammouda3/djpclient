#!/usr/bin/env python

from setuptools import setup, find_packages

from djpclient import version

setup(
    name = "djpclient",
    packages = ['djpclient',],
    version = version.VERSION,
    author = "Alan Illing",
    description = ("Django Profiler Client for profiling and application performance measurement services at djangoperformance.com"),
    license = "GPL",
    url = "https://github.com/ailling/djpclient",
    install_requires=['requests>=0.13.1', 'stopwatch>=0.3.1', 'Django>=1.3.1', 'python-memcached>=1.48', 'django-celery',]
)
