from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect




class LoginUser(LoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
