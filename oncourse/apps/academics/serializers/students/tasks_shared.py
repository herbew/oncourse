# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask

from oncourse.apps.academics.serializers.events import StudentEventSerializer
from oncourse.apps.masters.serializers.tasks import TaskSerializer

log = logging.getLogger(__name__)

class StudentEventTaskSerializer(serializers.ModelSerializer):
    student_event = StudentEventSerializer(required=True)
    task = TaskSerializer(required=True)
    
    class Meta:
        model = StudentEventTask
        fields = ['no', 'student_event', 'task', 'score' ]
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=self.model.objects.all(),
                fields=('student_event', 'task'),
                message=_("The Student, of Task already exists!")
            )
        ]