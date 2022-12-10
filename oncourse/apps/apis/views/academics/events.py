from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from oncourse.apps.academics.models.events import Event, StudentEvent
from oncourse.apps.apis.views.academics.students.permissions import(
    StudentPermission) 

from oncourse.apps.academics.serializers.events import StudentEventSerializer

log = logging.getLogger(__name__)

class StudentEventList(generics.ListAPIView):
    """Get Event base student(UserTraceAbility(user))
    """
    serializer_class = StudentEventSerializer
    permission_classes = [IsAuthenticated,StudentPermission]
    
    def get_queryset(self):
        
        queryset = StudentEvent.objects.filter(
            user_traceability__user=self.request.user)
        return queryset





