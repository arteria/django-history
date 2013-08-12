from django.db import models
from django.contrib.auth.models import User

HISTORY_EVENT_MODELS = ()

HISTORY_DISPLAY_TYPES = () 

class HistoryEvent(models.Model): 
    timestamp = models.DateTimeField()
    is_internal = models.BooleanField(default=False) 
    is_hidden = models.BooleanField(default=False) 
    app_model_obj = models.CharField(max_length=100, choices = HISTORY_EVENT_MODELS)
    obj_id = models.IntegerField(help_text="ID of the obj injected based on app_model_obj")
    display_as = models.CharField(max_length=100, choices = HISTORY_DISPLAY_TYPES, null=True, blank=True, default='')   

    def __unicode__(self):
        s =  ""+ str(self.timestamp)
        s += " " + self.app_model_obj + " (ID " + str(self.obj_id) + ") " + self.display_as
        return s


class History(models.Model):
    owner = models.ForeignKey(User, unique=True)
    events = models.ManyToManyField(HistoryEvent)

    def __unicode__(self):
        return self.owner.username + "'s History"
