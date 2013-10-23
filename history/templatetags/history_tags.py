from django import template
from django.template import RequestContext
from django.template import Context, Template
from django.utils.timesince import timesince
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaultfilters import safe
from django.template.loader import render_to_string

from datetime import datetime, timedelta
    
from history.models import History, HistoryEvent

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
    return safe("NULL<!-- NULL -->")
    
    
@register.filter
def showHistory(request, who, amount=10, pageIndex=1):
    if who == "anonymous":
        hs, created = History.objects.get_or_create(owner=None)
    else:
        # who is an username 
        hs, created = History.objects.get_or_create(owner__username=who)
    if created:            
        hs.save()
    isFirst = (pageIndex == 1) # could be used to show a header
    historyEvents = hs.events.filter(publish_timestamp__lte=datetime.utcnow()).exclude(is_hidden=True).exclude(is_internal=True).order_by("-event_timestamp")
    paginator = Paginator(historyEvents, amount)
    thisPage = paginator.page(pageIndex)
    hasMore = thisPage.has_next()
    listOfHistoryEvents = thisPage.object_list
    
    return safe(render_to_string('history/history.html', {'listOfHistoryEvents': listOfHistoryEvents,
                                                          'hasMore': hasMore,
                                                          'isFirst': isFirst,
                                                          'pageIndex': pageIndex,
                                                         }, context_instance=RequestContext(request)))
