# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from oncourse.apps.users.models.users import User



class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.types in ('001',):
            return reverse_lazy("staffs:master_company_list")
        
        logout(self.request)
        return reverse_lazy("account_login")
        
redirect = UserRedirectView.as_view()

class SignUpRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        list(messages.get_messages(self.request))
        messages.success(
            self.request, 
            _("Have successfully registered.") 
            )
        logout(self.request)
        return reverse_lazy("account_login")
        
signup_redirect = SignUpRedirectView.as_view()






