#!/usr/bin/env python

from distutils.core import setup

from djpclient import version

setup(
    name = "djpclient",
    packages = ['djpclient',],
    version = version.VERSION,
    author = "Alan Illing",
    description = ("Django Profiler Client for profiling and application performance measurement services at djangoperformance.com"),
    license = "GPL",
    url = "https://github.com/ailling/djpclient",
    install_requires=['requests>=0.13.1', 'simplejson=>2.3.0', 'stopwatch=>0.3.1'],
)
