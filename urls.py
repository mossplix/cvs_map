from django.conf.urls.defaults import *
from mapping.views.main import *
import os

ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(ROOT,'media')

urlpatterns = patterns(
    '',
    (r'^map/',map ),
    (r'^health_facilities',health_facilities),
    (r'^marker/(?P<radius>[\d]+)/(?P<color>[-a-z]+)/(?P<opacity>[\d]+)/marker.png', marker),
                         (r'^marker/(?P<radius>[\d]+)/(?P<color>[-a-z]+)/(?P<text>[-a-zA-Z0-9]+)/marker.png', marker),
                        (r'^marker/(?P<radius>[\d]+)/(?P<text>[-a-zA-Z0-9]+)/marker.png', marker),
                        (r'^marker/(?P<radius>[\d]+)/marker.png', marker),
     (r'^Media/(?P<path>.*)', 'django.views.static.serve',\
     {'document_root': MEDIA_PATH}),
     
    
    )
