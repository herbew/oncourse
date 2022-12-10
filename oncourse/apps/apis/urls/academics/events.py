from __future__ import unicode_literals, absolute_import

import logging

from django.urls import include, path

from oncourse.apps.apis.views.academics.events import StudentEventList

log = logging.getLogger(__name__)

urlpatterns = [
     path('my/event/', StudentEventList.as_view(), name='student_event'),
]