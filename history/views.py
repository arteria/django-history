from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.config import settings



from .templatetags.history_tags import showHistory
from .models import History

#TODO:
def displayHistory(request, anUser=None):
	'''
    Returns the first 10 events of the history for an user or the anonymous history.
    '''
    response = showHistory(request, anUser, amount=10, pageIndex=1)  # this is the history timeline as by using the template tag...
    return render_to_response('history/index.html', {})


#TODO:
def displayHistoryEvent(request, anUser=None, eventID=None):
    '''
    Detail (=landing page) for a particular event.
    '''
    return render_to_response('history/event.html', {})


def moreHistoryEvents(request, page=0,  who=None):
    '''
    Allow to append next events to the history using AJAX.
    '''
    page = int(page)
    if page == 0:
        response = ''  
    else:
        response = showHistory(request, who, amount=10, pageIndex=page) 
    return HttpResponse(safe(response), mimetype='text/html')  



