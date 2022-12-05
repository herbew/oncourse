# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.apps.academics.models.events import StudentEvent

from oncourse.apps.masters.models.tasks import Task

log = logging.getLogger(__name__)


class StudentEventTask(TimeStampedModel):
    """Student Event Task
    1. Task shared.
    2. Student do it.
    """
    ordered = models.IntegerField( 
            _("No"))
    
    student_event = models.ForeignKey(
        StudentEvent,
        on_delete=models.CASCADE,
        verbose_name=_("Student Event"),
        db_index=True)
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task"),
        db_index=True)
    
    score = models.IntegerField(default='0')
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'workbooks'
        verbose_name = u"StudentEventTask"
        verbose_name_plural = u"003 Workbooks Student Event Task"
        
        unique_together = (("student_event", "task", ),)

    def __init__(self, *args, **kwargs):
        super(StudentEventTask, self).__init__(*args, **kwargs)
        self._user_update = None
    
    def __str__(self):
        return "%s - %s" % (self.student_event, self.ordered)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(StudentEventTask, self).save(*args, **kwargs)
        
        
        
        
        
        
