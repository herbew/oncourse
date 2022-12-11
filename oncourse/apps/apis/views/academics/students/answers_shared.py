from __future__ import unicode_literals, absolute_import
import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import status, permissions, views, mixins, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import (MultiPartParser, FormParser, FileUploadParser,
            JSONParser
            )
from oncourse.apps.apis.views.academics.students.permissions import(
    StudentPermission) 

from oncourse.apps.masters.models.answers import Answer
from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask

from oncourse.apps.academics.models.students.answers_shared import (
    StudentEventTaskAnswer)

log = logging.getLogger(__name__)

class StudentEventTaskAnswerAPIView(views.APIView):
    """
    URL:
    ..... http://<domain/ip>/en-us/api/my/answer/ 
           
    method: POST
        
    Authorized :
    ..... Basic Auth(username, password)
            
    Parameters:
    ..... - data --Strings JSON for Answer submit
            
    ..........Example:
    ..............{
    .................."student_event_task__id": <int>,
    .................."answer__id":<int>
    ..............}
            
    """
    parser_classes = [JSONParser]
    permission_classes = [
                permissions.IsAuthenticated, 
                StudentPermission
                ]
    def get(self, request, *args, **kwargs):
        return Response(_("You have authorized user!"))
    
    def post(self, request, *args, **kwargs):
        
        data = request.data
        if data:
            student_event_task__id = data['student_event_task__id']
            answer__id = data['answer__id']
            
            try:
                student_event_task = StudentEventTask.objects.get(
                    id=student_event_task__id)
            except:
                return Response(
                    _("No Data of student_event_task__id!"), 
                    status=status.HTTP_400_BAD_REQUEST)   
                
            try:
                answer = Answer.objects.get(id=answer__id)
            except:
                return Response(
                    _("No Data of answer__id!"), 
                    status=status.HTTP_400_BAD_REQUEST) 
                
                
            seta, created = StudentEventTaskAnswer.objects.get_or_create(
                    student_event_task=student_event_task,
                    answer=answer
                )
            
            seta.user_updated = self.request.user.username
            seta.save()
            
            return Response(data, status=200)
        
        else:
            return Response(
                _("No Data Submitted!"), status=status.HTTP_400_BAD_REQUEST)    
        
        
        
        
        