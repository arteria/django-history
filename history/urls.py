from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns(
     '',
     (r'^load/',  'displayHistory', name='history_display'),
)

