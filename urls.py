from django.conf.urls.defaults import *
from mapping.views.main import *
import os

ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(ROOT, 'media')

urlpatterns = patterns(
    '',
    (r'^map/', map),
    (r'^health_facilities', health_facilities),
    (r'^births', births),
    (r'^epi/(?P<kind>[-a-z]+)', epi_kind),
    (r'^malnutrition', malnutrition),
    (r'^deaths', deaths),
    (r'^timemap', timeMap),
    (r'^getmessages', getMessages),
     (r'^Media/(?P<path>.*)', 'django.views.static.serve', \
     {'document_root': MEDIA_PATH}),
)

