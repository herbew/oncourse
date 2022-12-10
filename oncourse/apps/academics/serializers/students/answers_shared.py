# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.academics.models.students.answers_shared import (
    StudentEventTaskAnswerAnswer)

from oncourse.apps.masters.serializers.answers import AnswerSerializer
from oncourse.apps.academics.serializers.students.task_shared import StudentEventTaskSerializer

log = logging.getLogger(__name__)

class StudentEventTaskAnswerSerializer(serializers.ModelSerializer):
    student_event_task = StudentEventTaskSerializer(required=True)
    answer = AnswerSerializer(required=True)
    
    class Meta:
        model = StudentEventTaskAnswer
        fields = ['student_event_task', 'answer' ]
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=StudentEventTaskAnswer.objects.all(),
                fields=('student_event_task', 'answer' ),
                message=_("The Answer, of Task already exists!")
            )
        ]