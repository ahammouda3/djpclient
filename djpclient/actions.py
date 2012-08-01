
from django.utils import simplejson

import urllib, urllib2


import appsettings
from datetime import datetime

import tasks, send

import logging
logger = logging.getLogger(__name__)

import pdb

ALLOWED_KW_TYPES = (str, unicode, int, long, float,)


def _getviewname(sender=None):
    if sender is not None:
        return sender.__module__ + '.' + sender.__name__
    else:
        return ''


def CleanKwargs(kwargs):
    cleankwargs = {}
    for key, value in kwargs.items():
        if type(key) in ALLOWED_KW_TYPES and type(value) in ALLOWED_KW_TYPES:
            cleankwargs[str(key)] = str(value)
    return simplejson.dumps(cleankwargs)


def TransmitQueries(request, kwargs, queries, sender=None, name=''):
    "Sends query data to server"
    if queries is None:
        return
    
    if not name:
        name = _getviewname(sender)
        is_view = True
    else:
        is_view = False
    
    requestargs = simplejson.dumps(dict(request.GET))
    
    if appsettings.SEND_ASYNC:
        tasks.SendQueriesTask.delay(CleanKwargs(kwargs), requestargs, queries, name, is_view)
    else:
        send.SendQueries(CleanKwargs(kwargs), requestargs, queries, name, is_view)


def TransmitBenchmark(request, kwargs, exectime, cputime, sender=None, name=''):
    "Sends benchmark data to server"
    if exectime is None or exectime <= 0.0:
        return
    
    if not name:
        name = _getviewname(sender)
        is_view = True
    else:
        is_view = False
    
    requestargs = simplejson.dumps(dict(request.GET))
    
    if appsettings.SEND_ASYNC:
        tasks.SendBenchmarkTask.delay(CleanKwargs(kwargs), requestargs, exectime, cputime, name, is_view)
    else:
        send.SendBenchmark(CleanKwargs(kwargs), requestargs, exectime, cputime, name, is_view)



def TransmitMemcacheStats(request, kwargs, stats, sender=None, name=''):
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
    
    requestargs = simplejson.dumps(dict(request.GET))
    
    for stat in stats:
        if stat is None or stat.__class__.__name__ != 'MemcachedStats':
            continue
        
        if appsettings.SEND_ASYNC:
            tasks.SendMemcacheStat.delay(CleanKwargs(kwargs), requestargs, stat, name, is_view)
        else:
            send.SendMemcacheStat(CleanKwargs(kwargs), requestargs, stat, name, is_view)


def TransmitUserActivity(request, kwargs, sender=None, name=''):
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
    
    requestargs = simplejson.dumps(dict(request.GET))
    
    if appsettings.SEND_ASYNC:
        tasks.SendUserActivity(CleanKwargs(kwargs), requestargs, is_anonymous, username, userid, useremail, name, is_view)
    else:
        send.SendUserActivity(CleanKwargs(kwargs), requestargs, is_anonymous, username, userid, useremail, name, is_view)


def TransmitBundledData(request, kwargs, querydata, exectime, cputime, stat, sender):
    name = _getviewname(sender)
    
    is_anonymous = not request.user.is_authenticated()
    if is_anonymous:
        username = 'anonymous'
        userid = '-1'
        useremail = ''
    else:
        username = request.user.username
        userid = str(request.user.id)
        useremail = request.user.email
    
    requestargs = simplejson.dumps(dict(request.GET))
    
    if appsettings.SEND_ASYNC:
        tasks.SendBundle.delay(CleanKwargs(kwargs), requestargs, querydata, exectime, cputime, stat, is_anonymous, username, userid, useremail, name)
    else:
        send.SendBundle(CleanKwargs(kwargs), requestargs, querydata, exectime, cputime, stat, is_anonymous, username, userid, useremail, name)


def TransmitLogMessage(record):
    if appsettings.SEND_ASYNC:
        tasks.SendLogMessage(record)
    else:
        send.SendLogMessage(record)

