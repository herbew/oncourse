from __future__ import unicode_literals, absolute_import

from oncourse.libs.contrib.modeltranslation.translator import (
    TranslationOptions, translator)

from oncourse.apps.masters.models.courses import Course
from oncourse.apps.masters.models.tasks import Task
from oncourse.apps.masters.models.answers import Answer

# courses
class CourseTranslationOptions(TranslationOptions):
    fields = ('code','name', 'description' )
    
translator.register(Course, CourseTranslationOptions)

# tasks
class TaskTranslationOptions(TranslationOptions):
    fields = ('name', 'detailed' )
    
translator.register(Task, TaskTranslationOptions)

# answers
class AnswerTranslationOptions(TranslationOptions):
    fields = ('code', 'detailed' )
    
translator.register(Answer, AnswerTranslationOptions)