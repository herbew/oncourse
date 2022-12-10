from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import permissions

from oncourse.apps.workbooks.models.users import UserTraceability


class StudentPermission(permissions.BasePermission):
    """
    Student Permission
    """
    def has_permission(self, request, view):
        # Check UserTraceability if registered with self registered
        approved = UserTraceability.objects.filter(
            user=request.user).exists()
        
        return approved