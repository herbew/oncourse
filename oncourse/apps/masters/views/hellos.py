from __future__ import unicode_literals, absolute_import
"""
    https://django-rest-swagger.readthedocs.io/en/latest/
"""

import logging

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator

from rest_framework.views import APIView

from rest_framework_swagger import renderers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

log = logging.getLogger(__name__)

class JSONOpenAPIRender(renderers.OpenAPIRenderer):
    media_type = 'application/json'

class ApiHello(viewsets.ViewSet):
    """
    A simple ViewSet for test API Hello.
    """
    permission_classes = [permissions.AllowAny]
    # renderer_classes = [
    #     renderers.OpenAPIRenderer,
    #     # renderers.SwaggerUIRenderer,
    #     JSONOpenAPIRender
    # ]
    
    def list(self, request):
        # generator = SchemaGenerator(title='Crawler API')
        #
        # schema = generator.get_schema(
        #     request=request)
        
        return Response(dict(message="hallo"))
    
    
    