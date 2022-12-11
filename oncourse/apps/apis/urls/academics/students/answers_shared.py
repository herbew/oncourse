from __future__ import unicode_literals, absolute_import

import logging

from django.urls import include, path

from oncourse.apps.apis.views.academics.students.answers_shared import (
    StudentEventTaskAnswerAPIView)

log = logging.getLogger(__name__)

urlpatterns = [
     path('my/answer/submit/', StudentEventTaskAnswerAPIView.as_view(), name='student_answer'),
]