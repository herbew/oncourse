# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask

from oncourse.apps.masters.models.answers import Answer

log = logging.getLogger(__name__)


class StudentEventTaskAnswer(TimeStampedModel):
    """Student Event Task
    1. Task shared.
    2. Student do it.
    """
    student_event_task = models.ForeignKey(
        StudentEventTask,
        on_delete=models.CASCADE,
        verbose_name=_("Student Event Task"),
        db_index=True)
    
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name=_("Answer"),
        blank=True, null=True,
        db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'academics'
        verbose_name = u"StudentEventTaskAnswer"
        verbose_name_plural = u"004 Academics Student Event Task Answer"
        
        unique_together = (("student_event_task", "answer", ),)

    def __init__(self, *args, **kwargs):
        super(StudentEventTaskAnswer, self).__init__(*args, **kwargs)
        self._user_update = None
    
    def __str__(self):
        return "%s - %s" % (self.student_event_task, self.answer)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(StudentEventTaskAnswer, self).save(*args, **kwargs)
        
        
        
        
        
        
