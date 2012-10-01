#import base64, binascii
#import ast
from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from django.utils import simplejson

import appsettings
import memory, actions
#from djpclient.models import User
from djpclient.utils import format_data

import stopwatch, time, pdb, datetime

import logging
logger = logging.getLogger(__name__)


"For interacting with sessions outside of views"
#from django.contrib.sessions.backends.db import SessionStore
#from django.contrib.sessions.models import Session

class DJPClientMiddleware(object):
    def __init__(self):
        self.tracking_script_template = """                                                                                                                                      
        <script type="text/javascript">                                                                                                                                          
          var _gaq = _gaq || [];                                                                                                                                                 
          _gaq.push(['_setAccount', '%s']);                                                                                                                                      
          _gaq.push(['_trackPageview']);                                                                                                                                         
        
          (function() {                                                                                                                                                          
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;                                                                             
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';                                                    
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);                                                                                
          })();                                                                                                                                                                  
        
        _gaq.push(['_setCustomVar',                                                                                                                                              
              1,                   // This custom var is set to slot #1.  Required parameter.                                                                                    
              'GA-REPORTING-ID',           // The top-level name for your online content categories.  Required parameter.                                                        
              '%i',  // Sets the value of 'GA-REPORTING-ID' to take the session-id parameter for this particular aricle.  Required parameter.                                    
              1                    // (Optional) Sets the scope: 1:visitor-level; 2:session-level; 3:page-level;                                                                 
           ]);                                                                                                                                                                   
        </script>                                                                                                                                                                
        """
    
    def process_view(self, request, view, args, kwargs):
        
        logger.info('profile wrapper called')
        timer = stopwatch.Timer()
        
        cput1 = time.clock()
                        
        exectime = timer.stop()
        cput2 = time.clock()
        cputime = cput2 - cput1
        
        cookie_val=None
        cookie_expire=''
        '''
        if appsettings.TRACK_GOOGLE_ANALYTICS:
            "Again, once decorators get implemented, this portion of code
            require piping request.session info into the variables set above"
        '''
        response = view(request, *args, **kwargs)
        
        if appsettings.BUNDLE_DATA:
            actions.TransmitBundledData(request, kwargs,
                                        simplejson.dumps(connection.queries),
                                        exectime, cputime,
                                        memory.GetAggregateMemcacheStats(),
                                        sender=view,
                                        cookie=cookie_val, 
                                        ga_expiration_time=cookie_expire )
        else:
            if getattr(settings, 'PROFILE_QUERIES', True):
                actions.TransmitQueries(request, kwargs,
                                        queries=connection.queries,
                                        sender=view,
                                        cookie=cookie_val, 
                                        ga_expiration_time=cookie_expire)
                
            if getattr(settings, 'PROFILE_BENCHMARKS', True):
                actions.TransmitBenchmark(request, kwargs,
                                          exectime, cputime,
                                          sender=view,
                                          cookie=cookie_val, 
                                          ga_expiration_time=cookie_expire)
            
            if getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
                actions.TransmitMemcacheStats(request, kwargs,
                                              stats=memory.GetAggregateMemcacheStats(),
                                              sender=view,
                                              cookie=cookie_val, 
                                              ga_expiration_time=cookie_expire)
            
            if getattr(settings, 'PROFILE_USER_ACTIVITY', True):
                actions.TransmitUserActivity(request, kwargs,
                                             sender=view,
                                             cookie=cookie_val,
                                             ga_expiration_time=cookie_expire)
        return response
    
    
    def process_response(self, request, response):
        """
        Alters the response with the tracking script; the {% djp_ga_js_script %} inserts the
        html-frinedly placeholder, which is replaced by this process response if available
        """

        if appsettings.TRACK_GOOGLE_ANALYTICS:
            content = response.content
            index = content.find(appsettings.GA_JS_PLACEHOLDER)
            if index < 0:
                return response
            "Again, if decorators get going, we'll be stripping from request/response values ideally"
            newcontent = content.replace(
                appsettings.GA_JS_PLACEHOLDER, 
                self.tracking_script_template 
                %(appsettings.GA_PROFILE_ID, appsettings.GA_JS_PLACEHOLDER)
                )
            return HttpResponse(content=newcontent)
        else:
            return response
