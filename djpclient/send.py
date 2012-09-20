
from django.utils import simplejson

import appsettings
import requests
from datetime import datetime
from threading import Timer

import pdb

def _makerequest(data, endpoint):
    resp = requests.post(endpoint, data=simplejson.dumps(data),
                         headers={'content-type': 'application/json'})
    
    if appsettings.DEBUG:
        print 'endpoint %s response: %s' % (endpoint, str(resp))
    
    return resp


def SendData(data, endpoint):
    if not appsettings.SEND_IN_CELERY_QUEUE:
        t = Timer(appsettings.SEND_DELAY, _makerequest, args=(data, endpoint))
        t.start()
    else:
        _makerequest(data, endpoint)


def SendQueries(kwargs, requestargs, queries, name, is_view,
                ga_cookie, ga_exp_time):
    for query in queries:
        values = {'kwargs': kwargs,
                  'requestargs': requestargs,
                  
                  'appusername': appsettings.APP_USERNAME,
                  'appname': appsettings.APP_NAME,
                  'name': name,
                  'is_view': is_view,
                  'submission_timestamp': str(datetime.now()),
                  
                  'sql': query['sql'],
                  'execution_time': query['time'],
                  
                  'ga_id': ga_cookie,
                  'ga_expiration_time': str(ga_exp_time),
                  }
        
        SendData(values, appsettings.QUERY_ENDPOINT)


def SendBenchmark(kwargs, requestargs, exectime, cputime, viewname, ga_cookie, ga_exp_time, is_view=True):
    values = {'kwargs': kwargs,
              'requestargs': requestargs,
              
              'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              'name': viewname,
              'is_view': is_view,
              'submission_timestamp': str(datetime.now()),
              'execution_time': exectime,
              'cpu_time': cputime,
              
              'ga_id': ga_cookie,
              'ga_expiration_time': str(ga_exp_time),
              }
    
    SendData(values, appsettings.BENCHMARK_ENDPOINT)



def SendMemcacheStat(kwargs, requestargs, statobj, name, ga_cookie, ga_exp_time, is_view):
    values = {'kwargs': kwargs,
              'requestargs': requestargs,
              
              'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              'name': name,
              'is_view': is_view,
              'submission_timestamp': str(datetime.now()),
              
              'kilobytes': statobj.bytes / 1024.0,
              'connections': statobj.curr_connections,
              'kilobytes_read': statobj.bytes_read / 1024.0,
              'kilobytes_written': statobj.bytes_written / 1024.0,
              'limit_maxkb': statobj.limit_maxbytes / 1024.0,
              'hits': statobj.get_hits,
              'misses': statobj.get_misses,
              'get_commands': statobj.cmd_get,
              'set_commands': statobj.cmd_set,
              
              'ga_id': ga_cookie,
              'ga_expiration_time': str(ga_exp_time),
              }
    
    SendData(values, appsettings.MEMCACHESTAT_ENDPOINT)



def SendUserActivity(kwargs, requestargs, is_anonymous, username, userid, useremail, name, ga_cookie, ga_exp_time, is_view):
    values = {'kwargs': kwargs,
              'requestargs': requestargs,
              
              'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              'name': name,
              'is_view': is_view,
              'submission_timestamp': str(datetime.now()),
              
              'is_anonymous': is_anonymous,
              'websiteuserid': str(userid),
              'websiteusername': username,
              'websiteuseremail': useremail,
              
              'ga_id': ga_cookie,
              'ga_expiration_time': str(ga_exp_time),
              }
    
    SendData(values, appsettings.USER_ACTIVITY_ENDPOINT)



def SendUserConversion(kwargs, requestargs, is_anonymous, username, userid, useremail, name, is_view,
                       conversion_value=1.0, conversion_economic_value=0.0):
    raise Exception('not implemented yet')


def SendBundle(kwargs, requestargs, querydata, exectime, cputime, statobj, is_anonymous, username, userid, useremail, name, 
               ga_cookie, ga_exp_time, is_view=True):
    values = {'kwargs': kwargs,
              'requestargs': requestargs,
              'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              'name': name,
              'is_view': is_view,
              'submission_timestamp': str(datetime.now()),
              
              'querydata': querydata,
              
              'benchmark_execution_time': exectime,
              'benchmark_cpu_time': cputime,
              
              'kilobytes': statobj.bytes / 1024.0,
              'connections': statobj.curr_connections,
              'kilobytes_read': statobj.bytes_read / 1024.0,
              'kilobytes_written': statobj.bytes_written / 1024.0,
              'limit_maxkb': statobj.limit_maxbytes / 1024.0,
              'hits': statobj.get_hits,
              'misses': statobj.get_misses,
              'get_commands': statobj.cmd_get,
              'set_commands': statobj.cmd_set,
              
              'is_anonymous': is_anonymous,
              'websiteuserid': str(userid),
              'websiteusername': username,
              'websiteuseremail': useremail,
              
              'ga_id': ga_cookie,
              'ga_expiration_time': str(ga_exp_time),
              }

    SendData(values, appsettings.BUNDLED_DATA_ENDPOINT)


def SendLogMessage(record):
    values = {'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              
              'message': record.msg % record.args,
              'function_name': record.funcName,
              'logger_name': record.name,
              'level': record.levelname,
              'lineno': str(record.lineno),
              'module_name': record.module,
              
              'submission_timestamp': str(datetime.now()),
              }
    
    SendData(values, appsettings.LOG_MESSAGE_ENDPOINT)


