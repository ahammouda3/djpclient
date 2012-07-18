
import memcache, re
from django.conf import settings
from datetime import datetime, timedelta
              

class MemcachedStats:
    """
    Dynamically populated container of statistics from the memcache server
    """
    pass

def _query_memcache_server(location):
    try:
        host = memcache._Host(location)
        host.connect()
        host.send_cmd("stats")
        
        stats = MemcachedStats()
        
        while True:
            line = host.readline().split(None, 2)
            if line[0] == "END":
                break
            stat, key, value = line
            try:
                value = int(value)
                if key == "uptime":
                    value = timedelta(seconds=value)
                elif key == "time":
                    value = datetime.fromtimestamp(value)
            except ValueError:
                pass
            
            setattr(stats, key, value)
        
        host.close_socket()
        
        return stats
    except Exception:
        return None

def GetMemcacheStats():
    """
    Queries the memcache server for stats. Returns empty list if
    no CACHES (dictionary of dictionaries) are defined in settings.py
    """
    
    if not hasattr(settings, 'CACHES'):
        return None
    
    stats = []
    
    for key, value in settings.CACHES.items():
        backend = value.get('BACKEND', '')
        location = value.get('LOCATION', '')
        
        if backend.split('.')[-1] != 'MemcachedCache':
            continue
        else:
            stats.append(_query_memcache_server(location))
    
    return stats

def GetAggregateMemcacheStats():
    agg_stats = ('bytes', 'curr_connections', 'bytes_read', 'bytes_written',
             'get_hits', 'get_misses', 'cmd_get', 'cmd_set')
    max_stats = ('limit_maxbytes',)
    
    stats = GetMemcacheStats()
    agg = MemcachedStats()
    
    if stats:
        for stat in stats:
            for a in agg_stats:
                setattr(agg, a, getattr(agg, a, 0) + getattr(stat, a))
            for a in max_stats:
                setattr(agg, a, max(getattr(agg, a, 0), getattr(stat, a)))
    else:
        for a in agg_stats:
            setattr(agg, a, 0)
        for a in max_stats:
            setattr(agg, a, 0)
    
    return agg



