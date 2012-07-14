
import urllib, urllib2


import appsettings
from datetime import datetime

import simplejson
import tasks, send

import logging
logger = logging.getLogger(__name__)

import pdb

def _getviewname(sender=None):
    if sender is not None:
        return sender.__module__ + '.' + sender.__name__
    else:
        return ''



def TransmitQueries(request, queries, sender=None, name=''):
    "Sends query data to server"
    if queries is None:
        return
    
    if not name:
        name = _getviewname(sender)
        is_view = True
    else:
        is_view = False
    
    if appsettings.SEND_ASYNC:
        tasks.SendQueriesTask.delay(queries, name, is_view)
    else:
        send.SendQueries(queries, name, is_view)


def TransmitBenchmark(request, exectime, sender=None, name=''):
    "Sends benchmark data to server"
    if exectime is None or exectime <= 0.0:
        return
    
    if not name:
        name = _getviewname(sender)
        is_view = True
    else:
        is_view = False
    
    if appsettings.SEND_ASYNC:
        tasks.SendBenchmarkTask.delay(exectime, name, is_view)
    else:
        send.SendBenchmark(exectime, name, is_view)



def TransmitMemcacheStats(request, stats, sender=None, name=''):
    """
    Transmits profiled memcache data to djangoperformance.com
    """
    if stats is None:
        return
    
    if not name:
        name = _getviewname(sender)
        is_view = True
    else:
        is_view = False
    
    for stat in stats:
        if stat is None or stat.__class__.__name__ != 'MemcachedStats':
            continue
        
        if appsettings.SEND_ASYNC:
            tasks.SendMemcacheStat.delay(stat, name, is_view)
        else:
            send.SendMemcacheStat(stat, name, is_view)


def TransmitUserActivity(request, sender=None, name=''):
    if not name:
        name = _getviewname(sender)
        is_view = True
    else:
        is_view = False
    
    is_anonymous = not request.user.is_authenticated()
    if is_anonymous:
        username = 'anonymous'
        userid = '-1'
        useremail = ''
    else:
        username = request.user.username
        userid = str(request.user.id)
        useremail = request.user.email
    
    if appsettings.SEND_ASYNC:
        tasks.SendUserActivity(is_anonymous, username, userid, useremail, name, is_view)
    else:
        send.SendUserActivity(is_anonymous, username, userid, useremail, name, is_view)


