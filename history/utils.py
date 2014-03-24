from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import safe
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

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

def showFullStreamWrapper(request, arguments):
    '''
    Wrapper for showHistory
    0 : who
    1 : amount, eg. 10, 20, ..
    '''
    lArgs = arguments.split('|')
    lWho = lArgs[0]
    try:
        lAmount = int(lArgs[1])
    except:
        # default
        lAmount = 10
        
    return showAll(request, who=lWho, amount=lAmount, pageIndex=1)
    
    
def showUpcommingWrapper(request, arguments):
    '''
    Wrapper for showUpcomming
    0 : who
    1 : amount, eg. 10, 20, ..
    '''
    lArgs = arguments.split('|')
    lWho = lArgs[0]
    
    try:
        lAmount = int(lArgs[1])
    except:
        # default
        lAmount = 10
        
    return showUpcomming(request, who=lWho, amount=lAmount, pageIndex=1)
    
    

def showHistoryWrapper(request, arguments):
    '''
    Wrapper for showHistory
    0 : who
    1 : amount, eg. 10, 20, ..
    '''
    lArgs = arguments.split('|')
    lWho = lArgs[0]
    
    try:
        lAmount = int(lArgs[1])
    except:
        # default
        lAmount = 10
        
    return showHistory(request, who=lWho, amount=lAmount, pageIndex=1)
    


def showAll(request, who, amount=10, pageIndex=1):
    if who == "anonymous":
        hs, created = History.objects.get_or_create(owner=None)
    elif who == "auto":
        # automatically get username from request
        hs, created = History.objects.get_or_create(owner__username=request.user.username)
    else:
        # 'who' is an username (string)
        hs, created = History.objects.get_or_create(owner__username=who)
    if created:            
        hs.save()
    isFirst = (pageIndex == 1) # could be used to show a header
    
    allEvents = hs.events.all().exclude(is_hidden=True).exclude(is_internal=True).order_by('event_timestamp')
    paginator = Paginator(allEvents, amount)
    thisPage = paginator.page(pageIndex)
    hasMore = thisPage.has_next()
    return safe(render_to_string('history/stream.html', {'events': thisPage.object_list,
                                                          'hasMore': hasMore,
                                                          'isFirst': isFirst,
                                                          'pageIndex': pageIndex,
                                                         }, context_instance=RequestContext(request)))
                                                         
                                                         
                                                         
    
def showUpcomming(request, who, amount=10, pageIndex=1):
    if who == "anonymous":
        hs, created = History.objects.get_or_create(owner=None)
    elif who == "auto":
        # automatically get username from request
        hs, created = History.objects.get_or_create(owner__username=request.user.username)
    else:
        # 'who' is an username (string)
        hs, created = History.objects.get_or_create(owner__username=who)
    if created:            
        hs.save()
    isFirst = (pageIndex == 1) # could be used to show a header
    
    if getattr(settings, 'HISTORY_USE_UTC', False):
        now = datetime.utcnow()
    else:
        now = datetime.now()
        
    futureEvents = hs.events.filter(event_timestamp__gte=now).exclude(is_hidden=True).exclude(
        is_internal=True).order_by('event_timestamp')
    paginator = Paginator(futureEvents, amount)
    thisPage = paginator.page(pageIndex)
    hasMore = thisPage.has_next()
    listOfFutureEvents = thisPage.object_list
    
    return safe(render_to_string('history/upcomming.html', {'listOfFutureEvents': listOfFutureEvents,
                                                             'events': listOfFutureEvents,
                                                          'hasMore': hasMore,
                                                          'isFirst': isFirst,
                                                          'pageIndex': pageIndex,
                                                         }, context_instance=RequestContext(request)))
                                                         
        
                
def showHistory(request, who, amount=10, pageIndex=1):
    if who == "anonymous":
        hs, created = History.objects.get_or_create(owner=None)
    elif who == "auto":
        # automatically get username from request
        hs, created = History.objects.get_or_create(owner__username=request.user.username)
    else:
        # 'who' is an username (string)
        hs, created = History.objects.get_or_create(owner__username=who)
    if created:            
        hs.save()
    isFirst = (pageIndex == 1) # could be used to show a header
    
    if getattr(settings, 'HISTORY_USE_UTC', False):
        now = datetime.utcnow()
    else:
        now = datetime.now()
    
    # publish_timestamp or event_timestamp
    if getattr(settings, 'HISTORY_ORDER_BY', "publish_timestamp") == "publish_timestamp":
        historyEvents = hs.events.filter(publish_timestamp__lte=now).exclude(is_hidden=True).exclude(is_internal=True).extra(
                select={"tmpOrder":"COALESCE(is_sticky, publish_timestamp)"}, order_by=["-tmpOrder"])
    else:
        historyEvents = hs.events.filter(publish_timestamp__lte=now).exclude(is_hidden=True).exclude(is_internal=True).extra(
                select={"tmpOrder":"COALESCE(is_sticky, event_timestamp)"}, order_by=["-tmpOrder"])
                
    #historyEvents = hs.events.filter(publish_timestamp__lte=now).exclude(is_hidden=True).exclude(
    #    is_internal=True).order_by('-publish_timestamp', 'is_sticky')
    paginator = Paginator(historyEvents, amount)
    thisPage = paginator.page(pageIndex)
    hasMore = thisPage.has_next()
    listOfHistoryEvents = thisPage.object_list
    
    return safe(render_to_string('history/history.html', {'listOfHistoryEvents': listOfHistoryEvents,
                                                          'events': listOfHistoryEvents,
                                                          'hasMore': hasMore,
                                                          'isFirst': isFirst,
                                                          'pageIndex': pageIndex,
                                                         }, context_instance=RequestContext(request)))
