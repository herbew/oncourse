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
from oncourse.apps.academics.serializers.students.answers_shared import (
    StudentEventTaskAnswerSerializer)

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
    .................."option":None<Single Choice>, 0<unthik>, 1<thik>
    ..............}
            
    """
    parser_classes = [MultiPartParser,FormParser,JSONParser]
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
            option = data['option']
            
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
            
            # Get task typed,
            # TASK_TYPE_CHOICES = (
            #    ('01', _('Single-choice')),
            #    ('02', _('Multiple-choice')),
            # )
            typed_task = student_event_task.task.typed
            
            if typed_task == "02" and option in ('0',0):
                # Multiple Choice Cancel
                seta, created = StudentEventTaskAnswer.objects.get_or_create(
                        student_event_task=student_event_task,
                        answer=answer
                    )
                # Remove/Canceled
                seta.delete()
                
            elif typed_task == "02" and option in ('1',1):
                # Multiple Choice ADD
                seta, created = StudentEventTaskAnswer.objects.get_or_create(
                        student_event_task=student_event_task,
                        answer=answer
                    )
                seta.user_updated = self.request.user.username
                seta.save()
                
            else:
                try:
                    # Update answer
                    seta = StudentEventTaskAnswer.objects.get(
                        student_event_task=student_event_task)
                    seta.answer = answer
                    seta.user_updated = self.request.user.username
                    seta.save()
                    
                except:
                    # Create Single Choice
                    seta, created = StudentEventTaskAnswer.objects.get_or_create(
                        student_event_task=student_event_task,
                        answer=answer
                    )
                
                    seta.user_updated = self.request.user.username
                    seta.save()
            
            # Display Answer
            qs = StudentEventTaskAnswer.objects.filter(
                student_event_task=student_event_task)
            
            serializer = AnswerSerializer(instance=qs, many=True)
            
            return Response(serializer.data, status=200)
        
        else:
            return Response(
                _("No Data Submitted!"), status=status.HTTP_400_BAD_REQUEST)    
        
        
        
        
        