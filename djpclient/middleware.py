
from django.conf import settings
from django.db import connection
from django.utils import simplejson

import appsettings

import memory, actions
import stopwatch, time

import logging
logger = logging.getLogger(__name__)

import pdb

class DJPClientMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        logger.info('profile wrapper called')
        timer = stopwatch.Timer()
        
        cput1 = time.clock()
        
        response = view(request, *args, **kwargs)
        
        exectime = timer.stop()
        cput2 = time.clock()
        cputime = cput2 - cput1
        
        if appsettings.BUNDLE_DATA:
            actions.TransmitBundledData(request,
                                        simplejson.dumps(kwargs),
                                        simplejson.dumps(connection.queries),
                                        exectime, cputime,
                                        memory.GetAggregateMemcacheStats(),
                                        sender=view)
        else:
            if getattr(settings, 'PROFILE_QUERIES', True):
                actions.TransmitQueries(request,
                                        simplejson.dumps(kwargs),
                                        queries=connection.queries,
                                        sender=view)
            
            if getattr(settings, 'PROFILE_BENCHMARKS', True):
                actions.TransmitBenchmark(request,
                                          simplejson.dumps(kwargs),
                                          exectime, cputime,
                                          sender=view)
            
            if getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
                actions.TransmitMemcacheStats(request,
                                              simplejson.dumps(kwargs),
                                              stats=memory.GetAggregateMemcacheStats(), sender=view)
            
            if getattr(settings, 'PROFILE_USER_ACTIVITY', True):
                actions.TransmitUserActivity(request,
                                             simplejson.dumps(kwargs),
                                             sender=view)
        
        return response

