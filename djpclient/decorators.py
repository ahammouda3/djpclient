
from django.conf import settings
from django.db import connection
from django.utils import simplejson

from functools import wraps
import memory, actions

import appsettings

import stopwatch, time

import logging
logger = logging.getLogger(__name__)

import pdb

def profile(fn):
    def wrapped(request, *args, **kwargs):
        logger.info('profile wrapper called')
        timer = stopwatch.Timer()
        cput1 = time.clock()
        
        response = fn(request, *args, **kwargs)
        exectime = timer.stop()
        cput2 = time.clock()
        
        cputime = cput2 - cput1
        
        if appsettings.BUNDLE_DATA:
            actions.TransmitBundledData(request, kwargs,
                                        simplejson.dumps(connection.queries),
                                        exectime, cputime,
                                        memory.GetAggregateMemcacheStats(),
                                        sender=view)
        else:
            if getattr(settings, 'PROFILE_QUERIES', True):
                actions.TransmitQueries(request, kwargs,
                                        queries=connection.queries,
                                        sender=fn)
            
            if getattr(settings, 'PROFILE_BENCHMARKS', True):
                actions.TransmitBenchmark(request, kwargs,
                                          exectime=exectime, cputime=cputime,
                                          sender=fn)
            
            if getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
                actions.TransmitMemcacheStats(request, kwargs,
                                              stats=memory.GetMemcacheStats(),
                                              sender=fn)
            
            if getattr(settings, 'PROFILE_USER_ACTIVITY', True):
                actions.TransmitUserActivity(request, kwargs,
                                             sender=fn)
            
        return response
    
    return wrapped


def profile_components(components=[]):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            ls = map(lambda x: x.lower(), components)
            
            sql = 'sql' in ls or 'query' in ls or 'queries' in ls
            benchmark = 'benchmark' in ls or 'benchmarks' in ls
            memcache = 'memcached' in ls or 'memcache' in ls
            useractivity = 'useractivity' in ls or 'user activity' in ls
            
            if benchmark and getattr(settings, 'PROFILE_BENCHMARKS', True):
                timer = stopwatch.Timer()
                cput1 = time.clock()
                response = func(request, *args, **kwargs)
                exectime = timer.stop()
                cput2 = time.clock()
        
                cputime = cput2 - cput1
                
                actions.TransmitBenchmark(request, kwargs, exectime=exectime, cputime=cputime, sender=func)
                
            else:
                response = func(request, *args, **kwargs)
            
            
            if sql and getattr(settings, 'PROFILE_QUERIES', True):
                actions.TransmitQueries(request, kwargs,
                                        queries=connection.queries,
                                        sender=func)
            
            if memcache and getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
                actions.TransmitMemcacheStats(request, kwargs,
                                              stats=memory.GetMemcacheStats(),
                                              sender=func)
            
            if useractivity and getattr(settings, 'PROFILE_USER_ACTIVITY', True):
                actions.TransmitUserActivity(request, kwargs, sender=func)
            
            return response
        return wraps(func)(inner_decorator)
    return decorator





