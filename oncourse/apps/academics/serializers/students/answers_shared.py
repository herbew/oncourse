# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.academics.models.students.answers_shared import (
    StudentEventTaskAnswer)

from oncourse.apps.masters.serializers.answers import AnswerSerializer
from oncourse.apps.academics.serializers.students.tasks_shared import StudentEventTaskSerializer

log = logging.getLogger(__name__)

class StudentEventTaskAnswerSerializer(serializers.ModelSerializer):
    student_event_task = StudentEventTaskSerializer(required=True)
    
    answers = serializers.SerializerMethodField()
    
    def get_answers(self, obj):
        answer_id_list = [seta.answer.id for seta in 
            StudentEventTaskAnswer.objects.filter(student_event_task = 
            obj.student_event_task)]
        
        qs = Answer.objects.filter(id__in=answer_id_list).order_by("option")
        serializer = AnswerSerializer(instance=qs, many=True)
        return serializer.data
    
    class Meta:
        model = StudentEventTaskAnswer
        fields = ['student_event_task', 'answers' ]
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=StudentEventTaskAnswer.objects.all(),
                fields=('student_event_task', 'answer' ),
                message=_("The Answer, of Task already exists!")
            )
        ]