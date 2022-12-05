from __future__ import unicode_literals, absolute_import

from onevent.libs.contrib.modeltranslation.translator import (
    TranslationOptions, translator)

from onevent.apps.academics.models.events import Event
from oncourse.apps.academics.models.students.tasks_shared import StudentEventTask

# events
class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'date' )
    
translator.register(Event, EventTranslationOptions)

# student event tasks
class StudentEventTaskTranslationOptions(TranslationOptions):
    fields = ('no',  )
    
translator.register(StudentEventTask, StudentEventTaskTranslationOptions)