import datetime
from history.models import History, HistoryEvent
from django.contrib.contenttypes.models import ContentType


def createEvent(anUser, aModel, anId):
    ct = ContentType.objects.get_for_model(aModel)
    h = HistoryEvent(timestamp=datetime.now(), content_type=ct, object_id=anId)
    h.save()

def addEventToHistory(anEvent, anUser):
	hs, created = History.objects.get_or_create(owner=anUser)
	if created:
		hs.save()
	hs.events.add(anEvent)

