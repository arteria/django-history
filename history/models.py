from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


HISTORY_DISPLAY_TYPES = (('new_article', "Created New Article"),
                         )

class HistoryEvent(models.Model): 
    timestamp = models.DateTimeField()
    is_internal = models.BooleanField(default=False) 
    is_hidden = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    display_as = models.CharField(max_length=100, choices = HISTORY_DISPLAY_TYPES, null=True, blank=True, default='')   

    def __unicode__(self):
        return "%s from %s" %(str(self.content_type), str(self.timestamp.date()))


class History(models.Model):
    owner = models.ForeignKey(User, unique=True)
    events = models.ManyToManyField(HistoryEvent)

    def __unicode__(self):
        return "%s's History" %self.owner.username
