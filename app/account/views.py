from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordResetDoneView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
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


class ViewUserPasswordReset(PasswordResetView):
    template_name = 'account/reset/password_reset_form.html'
    email_template_name = 'account/reset/password_reset_email.html'
    success_url = reverse_lazy('account:reset_done')


class ViewUserPasswordChangeDone(PasswordResetDoneView):
    template_name = 'account/reset/password_reset_done.html'


class ViewUserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'account/reset/password_reset_confirm.html'
    success_url = reverse_lazy("account:reset_complete")


class ViewUserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/reset/password_reset_complete.html'


class ViewUserPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'

    def get_success_url(self):
        return reverse('account:view_info_user')
