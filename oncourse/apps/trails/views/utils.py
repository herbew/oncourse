from __future__ import unicode_literals, absolute_import

import logging

import tempfile
import shutil
import os 

from datetime import datetime

from django.conf import settings

from django.core.files.storage import default_storage

from oncourse.apps.trails.models.files import MetaFile
from oncourse.apps.trails.models.summernotes import MetaSummernote

log = logging.getLogger(__name__)

def trail_files_user_deleted(instance, url, username):
    """
    instance = Models sender,
    url = url from static dir/google drive
    username = username
    """
    ts = datetime.utcnow()
    try:
        mf = MetaFile.objects.get(
            meta_user=instance.user_update,
            meta_table=instance._meta.db_table,
            meta_raw_id="%s" % instance.pk,
            meta_file=url,
            defaults=dict(
                    meta_status="02", #deleted
                    meta_delete_ts=ts,
                    user_update=username
                )
            )
        
        
    except:
        for mf in MetaFile.objects.filter(
            meta_user=instance.user_update,
            meta_table=instance._meta.db_table,
            meta_raw_id=instance.pk
            ):
            if mf.meta_status in ('01',):
                mf.meta_status = "02" #deleted
                mf.meta_delete_ts = ts
                mf.user_update = username
                mf.save()
    
            
def trail_summernote_user_deleted(instance, fields, username):
    """
    instance = Models sender,
    fields = name fields of instance model
    username = username
    """
        
    ms, created = MetaSummernote.objects.get_or_create(
            meta_user=instance.user_update,
            meta_table=instance._meta.db_table,
            meta_raw_id="%s" % instance.pk,
            meta_field=fields,
            defaults=dict(
                meta_status="02",
                meta_delete_ts=datetime.utcnow(),
                user_update=username
                )
            )
    
    
    
def store_file_to_google_cloud(
        folder, 
        filename, 
        instance_field,
        instance):
    """Save file to google drive
    Input :
    - folder : the name of <field's name>_<model's name>
    - filename : the file name
    - instance_field : the field of instance object, example instance.resume_attachment
    - instance : instance object
    
    """
    
    #path is a name raw table save
    dirs = os.path.join(settings.MEDIA_ROOT, folder)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
     
    path = os.path.join(dirs, filename)
    
    #sha ----
    temp_dir = tempfile.mkdtemp()
     
    name = instance_field.name.split("/")
    index = 0 if len(name) == 0 else len(name) - 1
    name = name[index]
     
    temp_file = os.path.join(temp_dir, name)
         
    mode = 'a+' if os.path.exists(temp_file) else 'wb+'
    
     
    with open(temp_file, mode)  as destination:
        for chunk in instance_field.chunks():
            destination.write(chunk) 
 
    p = os.popen("sha1sum '%s'" % temp_file,"r")
    sh = p.read().split(" ")[0]
    p.close()
    shutil.rmtree(temp_dir)
    
    try:
        instance_field.storage = default_storage
        file_name = instance_field.storage.save(
            os.path.join(folder,filename), instance_field)
        url = instance_field.storage.url(file_name)
    except:
        instance_field.storage = settings.MEDIA_ROOT
        file_name = os.path.join(settings.MEDIA_ROOT, folder, filename)
        url = os.path.join(settings.MEDIA_ROOT, folder, filename)
    
    id = instance.pk if instance.pk else url
     
    mf, created = MetaFile.objects.get_or_create(
            meta_user=instance.user_update,
            meta_table=instance._meta.db_table,
            meta_raw_id="%s" % id,
            meta_file=url,
            defaults=dict(
                meta_file_name=os.path.join(folder,filename),
                meta_sha=sh,
                meta_size=instance_field.size
                )
            )
     
    
