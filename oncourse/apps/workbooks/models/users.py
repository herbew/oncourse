# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.core.choices import USER_CHOICES

from oncourse.apps.trails.models.summernotes import MetaSummernote
from oncourse.apps.trails.views.summernotes import clean_summernote_image
from oncourse.apps.trails.views.utils import trail_summernote_user_deleted

from oncourse.apps.users.models import User


log = logging.getLogger(__name__)


class UserTraceability(TimeStampedModel):
    """
        User possible a member as a Mentor or and a Student.
        the unique key (user, typed) --> one User with n typed(
        Only one typed in the same user)
    """
    USER_CHOICES = USER_CHOICES
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        db_index=True)
    
    typed = models.CharField( _("Type"), 
            choices=USER_CHOICES, 
            max_length=3,
            null=True, blank=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'workbooks'
        verbose_name = u"UserTraceability"
        verbose_name_plural = u"001 Workbooks User Traceability"
        
        unique_together = (("user", "typed", ),)

    def __init__(self, *args, **kwargs):
        super(UserTraceability, self).__init__(*args, **kwargs)
        self._user_update = None
    
    @property
    def get_typed(self):
        
        if not self.typed: return ""
        
        return dict(self.USER_CHOICES)[self.typed]
    
    def __str__(self):
        return "%s - %s" % (self.user, self.get_typed)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(UserTraceability, self).save(*args, **kwargs)
    
    
    
    
    











        
        
        
