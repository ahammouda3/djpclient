
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
    Queries the memcache server for stats. Returns None if
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



