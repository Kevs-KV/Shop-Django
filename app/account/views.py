from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from account.forms import AuthenticationUserForm, CreateUserForm


class ViewLoginUser(LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationUserForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(reverse('shop:product_list'))


class ViewInfoUser(TemplateView):
    template_name = 'account/info.html'


class ViewCreateUser(FormView):
    template_name = 'account/create.html'
    form_class = CreateUserForm

    def get_context_data(self, **kwargs):
        context = super(ViewCreateUser, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        User.objects.create_user(username, email, password)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('shop:product_list')
