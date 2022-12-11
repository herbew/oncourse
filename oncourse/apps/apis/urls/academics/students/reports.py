from __future__ import unicode_literals, absolute_import

import logging

from django.urls import include, path

from oncourse.apps.apis.views.academics.students.reports import (
    StudentEventTaskList)

log = logging.getLogger(__name__)

urlpatterns = [
     path('my/report/', StudentEventTaskList.as_view(), name='student_report'),
]