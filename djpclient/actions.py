from django.utils import simplejson

import urllib, urllib2


import appsettings
from datetime import datetime

import tasks, send

from decimal import Decimal
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

    if appsettings.SEND_IN_CELERY_QUEUE:
        tasks.SendQueriesTask.delay(CleanKwargs(kwargs), requestargs, queries, name, is_view=is_view,
                                    ga_exp_time=ga_expiration_time,
                                    ga_cookie=request.session['ga-report-id'] )
    else:
        send.SendQueries(CleanKwargs(kwargs), requestargs, queries, name, is_view=is_view,
                         ga_exp_time=ga_expiration_time,
                         ga_cookie=cookie )


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
    ga_expiration_time = Decimal(request.session.get_expiry_age())
    
    if appsettings.SEND_IN_CELERY_QUEUE:
        tasks.SendBenchmarkTask.delay(CleanKwargs(kwargs), requestargs, exectime, cputime, name, is_view=is_view,
                                      ga_exp_time=ga_expiration_time,
                                      ga_cookie=request.session['ga-report-id'] )
    else:
        #view = is_view
        send.SendBenchmark(CleanKwargs(kwargs), requestargs, exectime, cputime, name, is_view=is_view,
                           ga_exp_time=ga_expiration_time,
                           ga_cookie=request.session['ga-report-id'] ) 



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
    ga_expiration_time = Decimal(request.session.get_expiry_age())

    for stat in stats:
        if stat is None or stat.__class__.__name__ != 'MemcachedStats':
            continue
        
        if appsettings.SEND_IN_CELERY_QUEUE:
            tasks.SendMemcacheStat.delay(CleanKwargs(kwargs), requestargs, stat, name, is_view=is_view,
                                         ga_exp_time=ga_expiration_time,
                                         ga_cookie=request.session['ga-report-id'] ) 
        else:
            send.SendMemcacheStat(CleanKwargs(kwargs), requestargs, stat, name, is_view,
                                  ga_exp_time=ga_expiration_time,
                                  ga_cookie=request.session['ga-report-id'] ) 


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
    ga_expiration_time = Decimal(request.session.get_expiry_age())

    if appsettings.SEND_IN_CELERY_QUEUE:
        tasks.SendUserActivity(CleanKwargs(kwargs), requestargs, is_anonymous, username, userid, useremail, name, is_view=is_view,
                               ga_exp_time=ga_expiration_time,
                               ga_cookie=request.session['ga-report-id'] ) 
    else:
        send.SendUserActivity(CleanKwargs(kwargs), requestargs, is_anonymous, username, userid, useremail, name, is_view=is_view,
                              ga_exp_time=ga_expiration_time,
                              ga_cookie=request.session['ga-report-id'] ) 


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
    ga_expiration_time = Decimal(request.session.get_expiry_age())
    
    if appsettings.SEND_IN_CELERY_QUEUE:
        tasks.SendBundle.delay(CleanKwargs(kwargs), requestargs, querydata, exectime, cputime, stat, is_anonymous, username, userid, useremail, name,
                               ga_exp_time=ga_expiration_time,
                               ga_cookie=request.session['ga-report-id'] ) 
    else:
        send.SendBundle(CleanKwargs(kwargs), requestargs, querydata, exectime, cputime, stat, is_anonymous, username, userid, useremail, name,
                        ga_exp_time=ga_expiration_time,
                        ga_cookie=request.session['ga-report-id'] ) 
        


def TransmitLogMessage(record):
    if appsettings.SEND_IN_CELERY_QUEUE:
        tasks.SendLogMessage(record)
    else:
        send.SendLogMessage(record)

