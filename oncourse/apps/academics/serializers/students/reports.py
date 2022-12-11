# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.masters.models.tasks import Task
from oncourse.apps.masters.models.answers import Answer
from oncourse.apps.academics.models.events import StudentEvent
from oncourse.apps.academics.models.students.answers_shared import (
    StudentEventTaskAnswer)

from oncourse.apps.masters.serializers.courses import CourseSerializer
from oncourse.apps.workbooks.serializers.users import UserTraceabilitySerializer
from oncourse.apps.academics.serializers.events import EventSerializer

from oncourse.apps.masters.serializers.tasks import TaskSerializer
from oncourse.apps.masters.serializers.answers import AnswerSerializer

log = logging.getLogger(__name__)

class MyScore:
    def __init__(self, score=0):
        self.score = score

class MyScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField(default=0)

class MyTaskSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=True)
    typed = serializers.ChoiceField(choices=Task.TASK_TYPE_CHOICES)
    answers = serializers.SerializerMethodField()
    
    def get_answers(self, obj):
        qs = Answer.objects.filter(task=obj).order_by("option")
        serializer = AnswerSerializer(instance=qs, many=True)
        return serializer.data
    
    class Meta:
        model = Task
        fields = ['course', 'id', 'name', 'typed', 'detailed','answers']
        

class MyTaskAnswerSerializer(serializers.ModelSerializer):
    my_task = serializers.SerializerMethodField()
    my_answers = serializers.SerializerMethodField()
    my_score = serializers.SerializerMethodField()
    
    def get_my_task(self, obj):
        serializer = MyTaskSerializer(instance=obj.student_event_task.task)
        return serializer.data
    
    def get_my_answers(self, obj):
        answer_id_list = [seta.answer.id for seta in 
            StudentEventTaskAnswer.objects.filter(student_event_task = 
            obj.student_event_task)]
        
        qs = Answer.objects.filter(id__in=answer_id_list).order_by("option")
        serializer = AnswerSerializer(instance=qs, many=True)
        return serializer.data
    
    def get_my_score(self, obj):
        # answer correct id
        task = obj.student_event_task.task
        answer_id_correct = [answer.id for answer in Answer.objects.filter(
                task=task, is_correct=True)]
        
        score = 0
        for seta in StudentEventTaskAnswer.objects.filter(student_event_task = 
            obj.student_event_task):
            if seta.answer.id in answer_id_correct:
                score += seta.student_event_task.score
        
        serializer = MyScoreSerializer(MyScore(score=score))
        return serializer.data
    
    class Meta:
        model = StudentEventTaskAnswer
        fields = ['my_task', 'my_answers', 'my_score' ]

       
class ReportStudentSerializer(serializers.ModelSerializer):
    my_profile = serializers.SerializerMethodField()
    my_event = serializers.SerializerMethodField() 
    my_tasks = serializers.SerializerMethodField()
    
    def get_my_profile(self, obj):
        serializer = UserTraceabilitySerializer(instance=obj.user_traceability)
        return serializer.data
    
    def get_my_event(self, obj):
        serializer = EventSerializer(instance=obj.event)
        return serializer.data
        
    def get_my_tasks(self, obj):
        qs = StudentEventTaskAnswer.objects.filter(
            student_event_task__student_event=obj
            ).order_by("student_event_task__student_event__event__start_ts", 
                       "student_event_task__student_event__course__order_no")
        
        serializer = MyTaskAnswerSerializer(instance=qs, many=True)
        return serializer.data
    
    class Meta:
        model = StudentEvent
        fields = ['my_profile', 'my_event', 'my_tasks']
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        