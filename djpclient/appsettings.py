
"""
WARNING:
    nothing in this module should be changed; instead interact with settings.py
    and refer to the documentation at: http://djangoperformance.com/docs/
"""
DEBUG = False

from django.conf import settings

API_VERSION = 'v1'

APP_USERNAME = getattr(settings, 'DJP_APP_USERNAME', None)
APP_NAME = getattr(settings, 'DJP_APP_NAME', None)
API_KEY = getattr(settings, 'DJP_API_KEY', None)


if not APP_USERNAME:
    raise Exception("Django profiler client: Missing DJP_APP_USERNAME from your settings.py file")
if not APP_NAME:
    raise Exception("Django profiler client: Missing DJP_APP_NAME from your settings.py file")
if not API_KEY:
    raise Exception("Django profiler client: Missing DJP_API_KEY from your settings.py file")


SEND_IN_CELERY_QUEUE = getattr(settings, 'DJP_SEND_IN_CELERY_QUEUE', False)
SEND_DELAY = getattr(settings, 'DJP_SEND_DELAY', 1.0)


BUNDLE_DATA = getattr(settings, 'USE_BUNDLED_ENDPOINT', True)

if DEBUG:
    BASE_URL = 'http://localhost:8000'
else:
    BASE_URL = 'http://www.djangoperformance.com'




CREDENTIALS = 'username=%s&api_key=%s' % (APP_USERNAME, API_KEY)

QUERY_ENDPOINT = '%s/api/%s/query/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)
BENCHMARK_ENDPOINT = '%s/api/%s/benchmark/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)
MEMCACHESTAT_ENDPOINT = '%s/api/%s/memcachestat/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)
USER_ACTIVITY_ENDPOINT = '%s/api/%s/useractivity/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)
USER_CONVERSION_ENDPOINT = '%s/api/%s/userconversion/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)

BUNDLED_DATA_ENDPOINT = '%s/api/%s/clientappdata/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)

LOG_MESSAGE_ENDPOINT = '%s/api/%s/logmessage/?%s' % (BASE_URL, API_VERSION, CREDENTIALS)

