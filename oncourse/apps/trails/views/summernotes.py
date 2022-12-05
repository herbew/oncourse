# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import json
import os 
import uuid
import io

import tempfile
import shutil

from datetime import datetime
from html.parser import HTMLParser

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView

from oncourse.apps.trails.models.files import MetaFile
from oncourse.apps.trails.models.summernotes import MetaSummernote

log = logging.getLogger(__name__)
 
MAXIMUM_FILE_IMAGE = 300*1024

class AjaxDeleteFileView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        # Get url POST
        url = request.POST.get('url', '')
        
        # Tryong get name file
        url_split = url.split(settings.SEPARATOR)[0]
        name = url_split.split(settings.GOOGLE_CLOUD_PROJECT)[-1]
        
        storage_cloud = default_storage
        
        
        try:
            if storage_cloud.exists(name):
                storage_cloud.delete(name)
                context = dict(status=200,
                               content=_("Image have successfully deleted!"))
                
                # delete meta file
                for mf in MetaFile.objects.filter(meta_raw_id=url):
                    mf.delete()
            else:
                context = dict(status=201,
                               content=_("Any problem with source image file!"))
        
        except:
            # delete meta file
            for mf in MetaFile.objects.filter(meta_raw_id=url):
                mf.delete()
        
            
        return JsonResponse (context)
            
        
        
class AjaxUploadFileView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        
        def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE): 
            """Yield pieces of data from a file-like object until EOF.""" 
            while True: 
                chunk = file.read(size) 
                if not chunk: 
                    break 
                yield chunk
        
        #path is a name raw table save
        url = ""
        
        for f in request.FILES.getlist('files'):
            if int(f.size) > int(MAXIMUM_FILE_IMAGE):
                context = dict(status=201,
                               content="Maximum Image file is 300 KBytes!")
                return JsonResponse (context)
            
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            ext = f.name.split('.')[-1]
            filename = "%s.%s" % (uuid.uuid4(), ext)
            path = os.path.join('django-summernote', today, filename)
            
            
            #sha ----
            temp_dir = tempfile.mkdtemp()
            
            name = filename
            index = 0 if len(name) == 0 else len(name) - 1
            name = name[index]
            temp_file = os.path.join(temp_dir, name)
         
            mode = 'a+' if os.path.exists(temp_file) else 'wb+'
             
            with open(temp_file, mode)  as destination:
                for chunk in read_chunks(f):
                    destination.write(chunk) 
         
            p = os.popen("sha1sum '%s'" % temp_file,"r")
            sh = p.read().split(" ")[0]
            p.close()
            shutil.rmtree(temp_dir)
            
            storage_cloud = default_storage
            path_gs = storage_cloud.save(path, ContentFile(f.read()))
            url = storage_cloud.url(path_gs)
                    
            # Save at MetaFile
            mf, created = MetaFile.objects.get_or_create(
                meta_user="Summernote",
                meta_table=filename,
                meta_raw_id=url,
                meta_file=url,
                defaults=dict(
                    meta_file_name=filename,
                    meta_sha=sh,
                    meta_size = f.size
                    )
                )
            
            
        context = dict(url=url,path_gs=path_gs,
                       status=200)
        
        return JsonResponse (context)
    

class MyHtmlParser(HTMLParser):
    '''
    Parse simple url to extract data and image url.
    This is expecting a simple url containing only one data block and one iimage url.
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.image_url = []        
        self.no_img_html = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for a in attrs:
                if a[0] == 'src':
                    if not a[1] in self.image_url:
                        self.image_url.append(a[1])
        else:
            self.no_img_html += self.get_starttag_text()


    def handle_endtag(self, tag):
        if tag != 'img':
            self.no_img_html += '</%s>' % tag

    def handle_data(self, data):
        self.no_img_html += data
        self.text = data


def clean_summernote_image(html):
    """Clean all image before delete Summernote's field
    INPUT : html --<string of summernote field>
    OUTPUT : None
    """
    if html in (None,""):
        log.debug("No Html Fields")
        return
    
    # Call parser
    parser = MyHtmlParser()
    parser.feed(html)
    
    for url in parser.image_url:
        
        log.debug("Trying delete image %s" % (url))
        # Tryong get name file
        url_split = url.split(settings.SEPARATOR)[0]
        name = url_split.split(settings.GOOGLE_CLOUD_PROJECT)[-1]
        
        storage_cloud = default_storage
        
        try:
            if storage_cloud.exists(name):
                log.debug("delete image %s" % (name))
                storage_cloud.delete(name)
                
                # delete meta file
                for mf in MetaFile.objects.filter(meta_raw_id=url):
                    log.debug("delete MetaFile %s" % (url))
                    mf.delete()
            else:
                log.debug("no image %s" % (url))
        except:
            # delete meta file
            for mf in MetaFile.objects.filter(meta_raw_id=url):
                log.debug("delete MetaFile %s" % (url))
                mf.delete()
            
    