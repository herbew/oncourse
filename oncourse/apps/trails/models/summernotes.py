from __future__ import unicode_literals, absolute_import

import logging
import os

from datetime import datetime, timedelta
# Mongo
from mongoengine import connect, disconnect
from mongoengine import signals as mongo_signals
from bson import ObjectId

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_mongoengine import Document, EmbeddedDocument, fields

log = logging.getLogger(__name__)

#connect(settings.MONGODB_DATABASES['trails']['name'], alias='trails')
connect(db=settings.MONGODB_DATABASES['trails']['name'],
        host=settings.MONGODB_DATABASES['trails']['host'],
        username=settings.MONGODB_DATABASES['trails']['username'],
        password=settings.MONGODB_DATABASES['trails']['password'], alias='trails')

class MetaSummernote(Document):
    """File Size Inspection"""
    
    STATUS_CHOICES=(
        ('01','Active'),
        ('02','Deleted')
        )
    
#     id = fields.StringField(primary_key=True)
    
    meta_user = fields.StringField(max_length=30, blank=True, null=True)
    meta_table = fields.StringField(max_length=100, blank=True, null=True)
    meta_raw_id = fields.StringField(max_length=255, blank=True, null=True)
    meta_field = fields.StringField(max_length=255, blank=True, null=True) #file url
    
    meta_size = fields.IntField(dafault=0, blank=True, null=True)
    meta_status = fields.StringField( 
                max_length=2, 
                choices=STATUS_CHOICES,
                default='01')
    
    meta_delete_ts = fields.DateTimeField(null=True, blank=True)
    
    
    created = fields.DateTimeField(
        default=datetime.now(), editable=False,
    )
    
    updated = fields.DateTimeField(
        default=datetime.now(), editable=True,
    )
    
    user_update = fields.StringField(
            max_length=30, blank=True, null=True)
    
    meta = dict(
        db_alias='trails'
        )
    
    class Meta:
        app_label = 'trails'
        verbose_name = u"MetaSummernote"
        verbose_name_plural = u"Meta Summernote"
        
        ordering = ['meta_user', 'meta_table', 'meta_raw_id',
                    'meta_field', ]
        
        indexes = ['id', 'meta_user', 'meta_table', 'meta_raw_id', 'meta_field', 'user_update',
                   'meta_status']
        
        unique_together = (
            ("meta_user", "meta_table", "meta_raw_id", "meta_field"),)
        
        
    def __init__(self, *args, **kwargs):
        super(MetaSummernote, self).__init__(*args, **kwargs)
        self._updated_ts = datetime.now()
    
    def __str__(self):
        return "%s %s %s %s" % (self.meta_user, self.meta_table, 
                                self.meta_raw_id, self.meta_field)
    
    def save(self, *args, **kwargs):
        super(MetaSummernote, self).save(*args, **kwargs)
        
        self.updated = self._updated_ts
        
        
        
        
        
   