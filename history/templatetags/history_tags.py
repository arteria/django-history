from django import template
from django.template import RequestContext
from django.template import Context, Template
from django.utils.timesince import timesince
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaultfilters import safe
from django.template.loader import render_to_string
from django.conf import settings

from datetime import datetime, timedelta
    


from history.utils import showHistoryWrapper

register = template.Library()


@register.filter  
def renderHistoryEvent(request, historyEvent):
    '''
    '''
    try:
        return render_to_string(historyEvent.display_as, { 'obj': historyEvent.content_object,
                                                           'historyEvent': historyEvent,
                                                         }, context_instance=RequestContext(request))
    except Exception, ex:
        if settings.DEBUG:
            return "ERROR: ID=%s %s " % (str(historyEvent.id), str(ex))
        return "<!-- ERROR: %s -->" % str(ex)
    return safe("<!-- NULL -->")
    

# Allow to use showHistory as template tag
register.filter('showHistory', showHistoryWrapper)
register.filter('showUpcomming', showUpcommingWrapper)

