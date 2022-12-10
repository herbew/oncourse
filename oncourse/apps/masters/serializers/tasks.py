# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.masters.serializers.courses import CourseSerializer

from oncourse.apps.masters.models.tasks import Task


log = logging.getLogger(__name__)

class TaskSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=True)
    typed = serializers.ChoiceField(choices=Task.TASK_TYPE_CHOICES)
    class Meta:
        model = Task
        fields = ['course', 'name', 'typed', 'detailed']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=self.model.objects.all(),
                fields=('course', 'typed', 'name'),
                message=_("The Task typed of Course already exists!")
            )
        ]