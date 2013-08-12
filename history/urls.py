from django.conf.urls.defaults import *

urlpatterns = patterns('history.views',
    (r'^load/',  'displayHistory'),
)
