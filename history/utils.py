from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import safe
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType

from datetime import datetime, timedelta

from .models import History, HistoryEvent

 
def createEvent(aModel, anId):
    ct = ContentType.objects.get_for_model(aModel)
    h = HistoryEvent(content_type=ct, object_id=anId)
    h.save()
    return h


def getOrCreateEvent(aModel, anId):
    ct = ContentType.objects.get_for_model(aModel)
    h, created = HistoryEvent.objects.get_or_create(content_type=ct, object_id=anId)
    h.save()
    return h, created
     
    
def addEventToHistory(anEvent, anUser=None):
	hs, created = History.objects.get_or_create(owner=anUser)
	if created:
		hs.save()
	hs.events.add(anEvent)





def showHistory(request, who, amount=10, pageIndex=1):
    if who == "anonymous":
        hs, created = History.objects.get_or_create(owner=None)
    else:
        # 'who' is an username (string)
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