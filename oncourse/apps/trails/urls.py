# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path

from oncourse.apps.trails.views import summernotes

app_name = "trails"

urlpatterns = [
    #School
    path("ajax/summernotes/upload/files/", 
        view=summernotes.AjaxUploadFileView.as_view(),
        name="summernotes_upload_files"),
    
    path("ajax/summernotes/delete/files/", 
        view=summernotes.AjaxDeleteFileView.as_view(),
        name="summernotes_delete_files"),
    
    ]
