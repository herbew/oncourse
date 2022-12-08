from __future__ import unicode_literals, absolute_import

import logging
import os
import tempfile
import shutil

from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.apps.trails.models.summernotes import MetaSummernote
from oncourse.apps.trails.views.summernotes import clean_summernote_image
from oncourse.apps.trails.views.utils import trail_summernote_user_deleted


log = logging.getLogger(__name__)

class Course(TimeStampedModel):
    """
        Course is master course
    """
    
    code = models.CharField( 
            _("Code"), 
            unique=True, 
            max_length=255, 
            db_index=True)
    
    name = models.CharField( 
            _("Name"), 
            max_length=255, 
            db_index=True)
     
    description = models.TextField(
        _("Description"), 
        help_text=_("Course Description, Maximum 500 KBytes."),
        blank=True, 
        null=True)
    
    order_no = models.IntegerField(  
            _("Order No"), 
            default=0,
            help_text=_("Course ordered."), 
            )
    
    user_update = models.CharField(max_length=30, blank=True, null=True,
                                   db_index=True)


    class Meta:
        app_label = 'masters'
        verbose_name = u"Course"
        verbose_name_plural = u"001 Master Courses"
        
    def __init__(self, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)
        self._user_update = None
        

    def __str__(self):
       
        return "%s %s" % (self.code, self.name)

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user
    
    user_updated = property(get_user_update, set_user_update, None, "user_updated")
    
    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Course, self).save(*args, **kwargs)
        

def add_course(sender, instance, created, *args, **kwargs):
    """
    For trace ADD any files of description field
    Auto trail text
    """
        
    if not isinstance(instance, Course):
       return
    
    # if instance.description:
    #     meta_raw_id = "%s" % instance.pk
    #     ms, created = MetaSummernote.objects.get_or_create(
    #             meta_user=instance.user_update,
    #             meta_table=instance._meta.db_table,
    #             meta_raw_id=meta_raw_id,
    #             meta_field="description",
    #             defaults=dict(
    #                 meta_size=len(instance.description.encode('utf-8')),
    #                 user_update=instance.user_update
    #                 )
    #             )
    
post_save.connect(add_course, sender=Course)


def delete_course(sender, instance, *args, **kwargs):
    """
    For trace DELETE any files of description field
    Auto trail text -- deleted
    """
    if not isinstance(instance, Course):
        return
    
    
    # if instance.description:
    #     # Trail delete image summernote
    #     clean_summernote_image(instance.description)
    #
    #     # Trail delete
    #     trail_summernote_user_deleted(
    #         instance, 'description', instance.user_update)

        
pre_delete.connect(delete_course, sender=Course)



