from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from .models import History
 

def displayHistory(request, anUser=None):
	'''
    Returns the history for an user or the anonymous history.
    '''
    hs, created = History.objects.get_or_create(owner=anUser)
	return render_to_response('history/index.html', {'hs': hs, 'created': created})


def displayHistoryEvent(request, anUser=None, eventID=None):
    '''
    Detail (landing page) for a particular event.
    '''
    return render_to_response('history/event.html', {})