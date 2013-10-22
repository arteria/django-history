from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.translation import ugettext as _

import datetime
 
class HistoryEvent(models.Model): 
    event_timestamp = models.DateTimeField(help_text=_('When does it happen?'), default=datetime.datetime.utcnow())
    publish_timestamp = models.DateTimeField(help_text=_('When should this event show up in the timeline/history?'), default=datetime.datetime.utcnow())
    is_internal = models.BooleanField(default=False, help_text=_('By checking this, this event will never be shown to a user. Internal (system) usage only.')) 
    is_hidden = models.BooleanField(default=False, help_text=_('Allows the user to hide events from the timeline. Be careful with Anonymous History.'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    display_as = models.CharField(max_length=100, choices = getattr(settings, "HISTORY_DISPLAY_TYPES", ()), null=True, blank=True, default='')

    def __unicode__(self):
        return "%s from %s" %(str(self.content_type), str(self.event_timestamp.date()))


class History(models.Model):
    owner = models.ForeignKey(User, unique=True, null=True, blank=True)
    events = models.ManyToManyField(HistoryEvent)

    def __unicode__(self):
        if self.owner:
            return "%s's History" % self.owner.username
        return "Anonymous History"