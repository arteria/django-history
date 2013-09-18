from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from history.models import History
 
@login_required
def displayHistory(request):
	hs, created = History.objects.get_or_create(owner=request.user)
	print hs
	return render_to_response('history/index.html', {'hs': hs})
