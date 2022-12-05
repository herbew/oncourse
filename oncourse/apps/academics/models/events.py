# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.apps.workbooks.models.users import UserTraceability
from oncourse.apps.masters.models.courses import Course

log = logging.getLogger(__name__)


class Event(TimeStampedModel):
    """Event
    """
    name = models.CharField( 
            _("Name"), 
            max_length=255, 
            db_index=True)
    
    date_event = models.DateField( 
            _("Date Event"), null=True, blank=True)
    
    start_ts = models.DateTimeField( 
            _("Start Datetime"), 
            null=True, blank=True)
    
    end_ts = models.DateTimeField( 
            _("Finish Datetime"), 
            null=True, blank=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'academics'
        verbose_name = u"Event"
        verbose_name_plural = u"001 Academics Event"
        
        unique_together = (("name", "date_event", ),)

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._user_update = None
    
      
    def __str__(self):
        return "%s - %s" % (self.name, self.date_event)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Event, self).save(*args, **kwargs)
    
    
class StudentEvent(TimeStampedModel):
    """StudentEvent
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name=_("Event"),
        db_index=True)
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        db_index=True)
    
    user_traceability = models.ForeignKey(
        UserTraceability,
        on_delete=models.CASCADE,
        verbose_name=_("Student"),
        db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'academics'
        verbose_name = u"StudentEvent"
        verbose_name_plural = u"002 Academics Student Event"
        
        unique_together = (("event", "course", "user_traceability",  ),)

    def __init__(self, *args, **kwargs):
        super(StudentEvent, self).__init__(*args, **kwargs)
        self._user_update = None
    
      
    def __str__(self):
        return "%s:%s - %s" % (self.course, self.user_traceability.user.name, 
                            self.event)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(StudentEvent, self).save(*args, **kwargs)
    
    











        
        
        
