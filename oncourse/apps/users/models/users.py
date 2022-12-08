# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from datetime import datetime, timedelta, date

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from oncourse.core.choices import GENDER_CHOICES

log = logging.getLogger(__name__)


class User(AbstractUser):
    
    GENDER_CHOICES = GENDER_CHOICES
    
    name = models.CharField(
            _("Complete Name"), 
            max_length=250)
    
    birth_city = models.CharField(
            _("Birth City"), 
            max_length=100, 
            null=True, blank=True)
    
    birth_date = models.DateField(
            _("Birth Date"), 
            null=True, blank=True)
    
    gender = models.CharField( 
            _("Gender"), 
            choices=GENDER_CHOICES, 
            max_length=1, 
            null=True, blank=True)
    
    address = models.TextField(
            _("Address"), 
            null=True, blank=True)
    
    mobile = models.CharField( 
            _("Mobile"), 
            max_length=64, 
            null=True, blank=True)
    
    created = models.DateTimeField(
            _("Create"), 
            null=True, blank=True)
    
    modified = models.DateTimeField(
            _("Modified"), 
            null=True, blank=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)
    
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._user_update = None
         
    def __str__(self):
        
        if self.name:
            return self.name
        
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
    
    @property
    def get_address(self):
        return [a for a in self.address.split('\n') if not a in[None,""]]
    
    @property
    def get_email(self):
        
        if self.email:
            if len(self.email) > 26:
                return "%s --" % (self.email[:20])
            
        return self.email

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")
    
    def save(self, *args, **kwargs):
        
        if not self.pk:
            #created
            self.created = datetime.now()
            
        self.modified = datetime.now()
        
        self.user_update = self._user_update
        name = None
        if self.first_name:
            name = self.first_name
                
        if self.last_name:
            if name:
                name = "%s %s" % (name, self.last_name)
                
        if name:
            self.name = name
            
        super(User, self).save(*args, **kwargs)


def user_save(sender, instance, created, *args, **kwargs):
    
    from oncourse.apps.workbooks.models.users import UserTraceability
    
    if not isinstance(instance, User):
       return
    
    if created:
        usert = UserTraceability.objects.get_or_creater(
            user=instance, defaults=dict(typed="003"))
        
post_save.connect(user_save, sender=User)



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
