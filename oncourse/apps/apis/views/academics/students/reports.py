from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from oncourse.apps.academics.models.events import StudentEvent
from oncourse.apps.apis.views.academics.students.permissions import(
    StudentPermission) 

from oncourse.apps.academics.serializers.students.reports import (
    ReportStudentSerializer)

log = logging.getLogger(__name__)

class StudentEventTaskList(generics.ListAPIView):
    """
    URL:
    ..... http://<domain/ip>en-us/api/my/report/ 
           
    method: GET
        
    Authorized :
    ..... Basic Auth(username, password)
            
    Return:
    .... - IF error(JSON(content, status))
    .... - JSON(serializer(ReportStudentSerializer), status=200)
    .
    .
    .
            
    """
    serializer_class = ReportStudentSerializer
    permission_classes = [IsAuthenticated, StudentPermission]
    
    def get_queryset(self):
        
        queryset = StudentEvent.objects.filter(
            user_traceability__user=self.request.user
            ).order_by("event__start_ts", "course__order_no")
            
        return queryset
