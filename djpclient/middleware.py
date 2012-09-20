from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from django.utils import simplejson

import appsettings
import memory, actions
from djpclient.models import User

import stopwatch, time, pdb, datetime

import logging
logger = logging.getLogger(__name__)


"For interacting with sessions outside of views"
from django.contrib.sessions.backends.db import SessionStore

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
        
        response = view(request, *args, **kwargs)
        
        exectime = timer.stop()
        cput2 = time.clock()
        cputime = cput2 - cput1

        if not request.session.get('ga-report-id'):
            '''
            Create Reporting Id to be injected into ga.js in process_response,
            and save it as a session variable on a day by day basis.

            The session data now gets passed to transmit functions
            through the request object.
            '''
            now=datetime.datetime.now()
            lifetime=( datetime.datetime(now.year, now.month, now.day +1, 0) - now ).total_seconds()
            new_user = User(creation_time=now,expiration_time=lifetime ) #Change to User.objects.create(params*) if time
            new_user.save()

            request.session.__setitem__('ga-report-id', new_user.analytics_id)
            request.session.set_expiry( lifetime )
        
        if appsettings.BUNDLE_DATA:
            actions.TransmitBundledData(request, kwargs,
                                        simplejson.dumps(connection.queries),
                                        exectime, cputime,
                                        memory.GetAggregateMemcacheStats(),
                                        sender=view)
        else:
            if getattr(settings, 'PROFILE_QUERIES', True):
                actions.TransmitQueries(request, kwargs,
                                        queries=connection.queries,
                                        sender=view)
                
            if getattr(settings, 'PROFILE_BENCHMARKS', True):
                actions.TransmitBenchmark(request, kwargs,
                                          exectime, cputime,
                                          sender=view)
            
            if getattr(settings, 'PROFILE_MEMCACHE_STATS', True):
                actions.TransmitMemcacheStats(request, kwargs,
                                              stats=memory.GetAggregateMemcacheStats(),
                                              sender=view)
            
            if getattr(settings, 'PROFILE_USER_ACTIVITY', True):
                actions.TransmitUserActivity(request, kwargs,
                                             sender=view)

        return response
    
    def process_response(self, request, response):
        """
        Alters the response with the tracking script; the {% djp_ga_js_script %} inserts the
        html-frinedly placeholder, which is replaced by this process response if available
        """
        # Should pull out previously set cookie (GA-ACCOUNTS-ID) to be injected into ga.js
        # This should then be injected into a google analytics custom variable
        
        # Therefore, need to see what kind of access one can have with google analytics custom vars
        # Also need to look into persistence of session-vars as a user navigates around a site
        # ....
        
        content = response.content
        index = content.find(appsettings.GA_JS_PLACEHOLDER)
        
        if index < 0:
            return response
        newcontent = content.replace(appsettings.GA_JS_PLACEHOLDER, 
                                     self.tracking_script_template %(appsettings.GA_PROFILE_ID, request.session['ga-report-id'] )
                                     )
        return HttpResponse(content=newcontent)
