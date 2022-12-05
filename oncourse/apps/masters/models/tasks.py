# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.core.choices import TASK_TYPE_CHOICES

from oncourse.apps.trails.models.summernotes import MetaSummernote
from oncourse.apps.trails.views.summernotes import clean_summernote_image
from oncourse.apps.trails.views.utils import trail_summernote_user_deleted

from oncourse.apps.masters.models.courses import Course


log = logging.getLogger(__name__)

class Task(TimeStampedModel):
    TASK_TYPE_CHOICES = TASK_TYPE_CHOICES
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        db_index=True)
    
    name = models.CharField(
            _("Name"),
            max_length=255, 
            db_index=True)
    
    typed = models.CharField( 
            _("Typed"), 
            max_length=2, 
            choices=TASK_TYPE_CHOICES,
            db_index=True)
    
    detailed = models.TextField(
        _("Detail Task"), 
        help_text=_("Detail Task, Maximum 500 KBytes."),
        blank=True, 
        null=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Task"
        verbose_name_plural = u"002 Master Tasks"
        
        unique_together = (("course", "typed", "name"),)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self._user_update = None
    
    def __str__(self):
        return self.name
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Task, self).save(*args, **kwargs)

def add_task(sender, instance, created, *args, **kwargs):
    """
    For trace ADD any files of detailed field
    Auto trail text
    """
        
    if not isinstance(instance, Task):
       return
    
    if instance.detailed:
        meta_raw_id = "%s" % instance.pk
        ms, created = MetaSummernote.objects.get_or_create(
                meta_user=instance.user_update,
                meta_table=instance._meta.db_table,
                meta_raw_id=meta_raw_id,
                meta_field="detailed",
                defaults=dict(
                    meta_size=len(instance.detailed.encode('utf-8')),
                    user_update=instance.user_update
                    )
                )
    
post_save.connect(add_task, sender=Task)


def delete_task(sender, instance, *args, **kwargs):
    """
    For trace DELETE any files of detailed field
    Auto trail text -- deleted
    """
    if not isinstance(instance, Task):
        return
    
    
    if instance.detailed:
        # Trail delete image summernote
        clean_summernote_image(instance.detailed)
        
        # Trail delete
        trail_summernote_user_deleted(
            instance, 'detailed', instance.user_update)

        
pre_delete.connect(delete_task, sender=Task)










        
        
        
