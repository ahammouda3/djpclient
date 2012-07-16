
import appsettings
import requests
import simplejson
from datetime import datetime

import pdb

def SendQueries(queries, name, is_view):
    for query in queries:
        values = {'appusername': appsettings.APP_USERNAME,
                  'appname': appsettings.APP_NAME,
                  'name': name,
                  'is_view': is_view,
                  'submission_timestamp': str(datetime.now()),
                  
                  'sql': query['sql'],
                  'execution_time': query['time'],
                  }
        print 'sending query to %s' % appsettings.QUERY_ENDPOINT
        
        resp = requests.post(appsettings.QUERY_ENDPOINT,
                             data=simplejson.dumps(values),
                             headers={'content-type': 'application/json'})
        print 'query endpoint response: ', resp


def SendBenchmark(exectime, cputime, viewname, is_view=True):
    values = {'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              'name': viewname,
              'is_view': is_view,
              'submission_timestamp': str(datetime.now()),
              'execution_time': exectime,
              'cpu_time': cputime
              }
    resp = requests.post(appsettings.BENCHMARK_ENDPOINT,
                         data=simplejson.dumps(values),
                         headers={'content-type': 'application/json'})
    
    print 'benchmark endpoint response: ', resp


def SendMemcacheStat(statobj, name, is_view):
    values = {'appusername': appsettings.APP_USERNAME,
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
              'set_commands': statobj.cmd_set
              }
    
    resp = requests.post(appsettings.MEMCACHESTAT_ENDPOINT,
                         data=simplejson.dumps(values),
                         headers={'content-type': 'application/json'})
    
    print 'memcachestats endpoint response: ', resp


def SendUserActivity(is_anonymous, username, userid, useremail, name, is_view):
    values = {'appusername': appsettings.APP_USERNAME,
              'appname': appsettings.APP_NAME,
              'name': name,
              'is_view': is_view,
              'activity_timestamp': str(datetime.now()),
              
              'is_anonymous': is_anonymous,
              'websiteuserid': str(userid),
              'websiteusername': username,
              'websiteuseremail': useremail,
              }
    
    resp = requests.post(appsettings.USER_ACTIVITY_ENDPOINT,
                         data=simplejson.dumps(values),
                         headers={'content-type': 'application/json'})
    
    print 'useractivity endpoint response: ', resp


def SendUserConversion(is_anonymous, username, userid, useremail, name, is_view,
                       conversion_value=1.0, conversion_economic_value=0.0):
    raise Exception('not implemented yet')


