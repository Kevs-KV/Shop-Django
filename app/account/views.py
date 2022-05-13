from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse

from account.forms import AuthenticationUserForm


class LoginUser(LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationUserForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(reverse('shop:product_list'))
