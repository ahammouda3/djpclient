
from django.conf import settings
from django.db import connection
import memory, actions, stopwatch

import logging
logger = logging.getLogger(__name__)

import pdb

class DJPClientMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        logger.info('profile wrapper called')
        timer = stopwatch.Timer()
        
        response = view(request, *args, **kwargs)
        time = timer.stop()
        
        if getattr(settings, 'PROFILE_QUERIES', True):
            actions.TransmitQueries(request,
                                    queries=connection.queries,
                                    sender=view)
        
        if getattr(settings, 'PROFILE_BENCHMARKS', True):
            actions.TransmitBenchmark(request,
                                      exectime=time, sender=view)
        
        if getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
            actions.TransmitMemcacheStats(request, stats=memory.GetMemcacheStats(), sender=view)
        
        if getattr(settings, 'PROFILE_USER_ACTIVITY', True):
            actions.TransmitUserActivity(request, sender=view)
        
        return response
