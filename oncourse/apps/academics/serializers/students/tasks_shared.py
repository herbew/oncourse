# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask
from oncourse.apps.masters.models.answers import Answer


from oncourse.apps.academics.serializers.events import StudentEventSerializer
from oncourse.apps.masters.serializers.tasks import TaskSerializer
from oncourse.apps.masters.serializers.answers import AnswerSerializer

log = logging.getLogger(__name__)

class StudentEventTaskSerializer(serializers.ModelSerializer):
    student_event = StudentEventSerializer(required=True)
    task = TaskSerializer(required=True)
    answers = serializers.SerializerMethodField(required=True)
    
    def get_answers(self, task):
        qs = Answer.objects.filter(task=task)
        serializer = AnswerSerializer(instance=qs, many=True)
        return serializer.data
    
    class Meta:
        model = StudentEventTask
        fields = ['id','no', 'student_event', 'task', 'score', 'answers' ]
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=StudentEventTask.objects.all(),
                fields=('student_event', 'task'),
                message=_("The Student, of Task already exists!")
            )
        ]