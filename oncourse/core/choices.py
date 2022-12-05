from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


USER_CHOICES = (
        ('001', _('Admin')),
        ('002', _('Mentor')),
        ('003', _('Student')),
     )

GENDER_CHOICES = (
        ('m',_('Male')),
        ('f',_('Female')),
    )

TASK_TYPE_CHOICES = (
        ('01', _('Single-choice')),
        ('02', _('Multiple-choice')),
     )

TASK_OPTION_CHOICES = (
        ('', _('Multiple-choice')),
        ('A', _('A')),
        ('B', _('B')),
        ('C', _('C')),
        ('D', _('D')),
        ('E', _('E')),
     )















