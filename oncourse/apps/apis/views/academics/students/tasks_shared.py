from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask
from oncourse.apps.apis.views.academics.students.permissions import(
    StudentPermission) 

from oncourse.apps.academics.serializers.students.tasks_shared import (
    StudentEventTaskSerializer)

log = logging.getLogger(__name__)

class StudentEventTaskList(generics.ListAPIView):
    """
    URL:
    ..... http://<domain/ip>en-us/api/my/<course code>/task/ 
           
    method: GET
        
    Authorized :
    ..... Basic Auth(username, password)
            
    Parameter url kwarg:
    ..... - course_code --Strings Course Code
    
    Return:
    .... - IF error(JSON(content, status))
    .... - JSON(serializer(StudentEventTaskSerializer), status=200)
    .
    .
    .
            
    """
    serializer_class = StudentEventTaskSerializer
    permission_classes = [IsAuthenticated, StudentPermission]
    
    lookup_url_kwarg = "course_code"
    
    def get_queryset(self):
        
        queryset = StudentEventTask.objects.filter(
            student_event__user_traceability__user=self.request.user,
            task__course__code=self.kwargs.get('course_code')
            ).order_by("no")
            
        return queryset
