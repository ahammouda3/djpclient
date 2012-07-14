
from django.conf import settings
from django.db import connection
from functools import wraps
import memory, actions


import stopwatch

import logging
logger = logging.getLogger(__name__)

import pdb

def profile(fn):
    def wrapped(request, *args, **kwargs):
        logger.info('profile wrapper called')
        timer = stopwatch.Timer()
        
        response = fn(request, *args, **kwargs)
        time = timer.stop()
        
        if getattr(settings, 'PROFILE_QUERIES', True):
            actions.TransmitQueries(request,
                                    queries=connection.queries,
                                    sender=fn)
        
        if getattr(settings, 'PROFILE_BENCHMARKS', True):
            actions.TransmitBenchmark(request,
                                      exectime=time, sender=fn)
        
        if getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
            actions.TransmitMemcacheStats(request, stats=memory.GetMemcacheStats(), sender=fn)
        
        if getattr(settings, 'PROFILE_USER_ACTIVITY', True):
            actions.TransmitUserActivity(request, sender=fn)
        
        return response
    
    return wrapped


def profile_components(components=[]):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            ls = map(lambda x: x.lower(), components)
            
            sql = 'sql' in ls or 'query' in ls
            benchmark = 'benchmark' in ls
            memcache = 'memcached' in ls or 'memcache' in ls
            useractivity = 'useractivity' in ls or 'user activity' in ls
            
            if benchmark and getattr(settings, 'PROFILE_BENCHMARKS', True):
                timer = stopwatch.Timer()
                response = func(request, *args, **kwargs)
                time = timer.stop()
                
                actions.TransmitBenchmark(request, exectime=time, sender=func)
                
            else:
                response = func(request, *args, **kwargs)
            
            
            if sql and getattr(settings, 'PROFILE_QUERIES', True):
                actions.TransmitQueries(request,
                                        queries=connection.queries,
                                        sender=func)
            
            if memcache and getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
                actions.TransmitMemcacheStats(request,
                                              stats=memory.GetMemcacheStats(),
                                              sender=func)
            
            if useractivity and getattr(settings, 'PROFILE_USER_ACTIVITY', True):
                actions.TransmitUserActivity(request, sender=func)
            
            return response
        return wraps(func)(inner_decorator)
    return decorator





