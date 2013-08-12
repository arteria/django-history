from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from history.models import History
 
@login_required
def displayHistory(request):
	pass
