# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.core.choices import TASK_OPTION_CHOICES

from oncourse.apps.trails.models.summernotes import MetaSummernote
from oncourse.apps.trails.views.summernotes import clean_summernote_image
from oncourse.apps.trails.views.utils import trail_summernote_user_deleted

from oncourse.apps.masters.models.tasks import Task


log = logging.getLogger(__name__)

class Answer(TimeStampedModel):
    
    TASK_OPTION_CHOICES = TASK_OPTION_CHOICES
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task"),
        db_index=True)
    
    code = models.CharField( 
            _("Code"), 
            help_text=_("Option answer signed."),
            max_length=255, 
            db_index=True)
    
    option = models.CharField( 
            _("Option"), 
            max_length=1, 
            choices=TASK_OPTION_CHOICES,
            db_index=True)
    
    detailed = models.TextField(
        _("Detail Answer"), 
        help_text=_("Detail Answer, Maximum 500 KBytes."),
        blank=True, 
        null=True)
    
    # Correct Answer
    is_correct = models.BooleanField(
        _("Is Correct Answer?"), 
        default=False)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Answer"
        verbose_name_plural = u"003 Master Answers"
        
        unique_together = (("task", "code", ),)

    def __init__(self, *args, **kwargs):
        super(Answer, self).__init__(*args, **kwargs)
        self._user_update = None
    
    def __str__(self):
        return "%s-%s" % (self.task, self.code)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Answer, self).save(*args, **kwargs)

def add_task(sender, instance, created, *args, **kwargs):
    """
    For trace ADD any files of detailed field
    Auto trail text
    """
        
    if not isinstance(instance, Answer):
       return
    
    # if instance.detailed:
    #     meta_raw_id = "%s" % instance.pk
    #     ms, created = MetaSummernote.objects.get_or_create(
    #             meta_user=instance.user_update,
    #             meta_table=instance._meta.db_table,
    #             meta_raw_id=meta_raw_id,
    #             meta_field="detailed",
    #             defaults=dict(
    #                 meta_size=len(instance.detailed.encode('utf-8')),
    #                 user_update=instance.user_update
    #                 )
    #             )
    
post_save.connect(add_task, sender=Answer)


def delete_task(sender, instance, *args, **kwargs):
    """
    For trace DELETE any files of detailed field
    Auto trail text -- deleted
    """
    if not isinstance(instance, Answer):
        return
    
    
    # if instance.detailed:
    #     # Trail delete image summernote
    #     clean_summernote_image(instance.detailed)
    #
    #     # Trail delete
    #     trail_summernote_user_deleted(
    #         instance, 'detailed', instance.user_update)

        
pre_delete.connect(delete_task, sender=Answer)










        
        
        
