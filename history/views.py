from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from .models import History
 
@login_required
def displayHistory(request, user=None):
	'''
    Returns the history for an user or the anonymous history.
    '''
    hs, created = History.objects.get_or_create(owner=user)
	return render_to_response('history/index.html', {'hs': hs, 'created': created})
