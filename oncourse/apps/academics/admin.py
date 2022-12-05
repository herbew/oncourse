# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from oncourse.apps.academics.models.events import Event, StudentEvent
from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask
from oncourse.apps.academics.models.students.answer_shared import (
    StudentEventTaskAnswer)

admin.site.register(Event)
admin.site.register(StudentEvent)

admin.site.register(StudentEventTask)
admin.site.register(StudentEventTaskAnswer)



