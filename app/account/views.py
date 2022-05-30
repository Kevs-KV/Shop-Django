from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordResetDoneView, UserModel
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, FormView

from account.forms import AuthenticationUserForm, UserPasswordResetForm, SignupForm
from account.token import TokenGenerator


class ViewLoginUser(LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationUserForm

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(reverse('shop:product_list'))


class ViewInfoUser(TemplateView):
    template_name = 'account/info.html'


class ViewSignupUser(FormView):
    template_name = 'account/create.html'
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('account/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': TokenGenerator().make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


class ViewUserSingupActivate(View):

    def dispatch(self, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])
        if user is not None and TokenGenerator().check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            return HttpResponse(reverse('shop:product_list'))
        else:
            return HttpResponse('Activation link is invalid!')

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                UserModel.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


# class ViewCreateUser(FormView):
#     template_name = 'account/create.html'
#     form_class = CreateUserForm
#
#     def get_context_data(self, **kwargs):
#         context = super(ViewCreateUser, self).get_context_data(**kwargs)
#         context['form'] = self.form_class
#         return context
#
#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         User.objects.create_user(username, email, password)
#         return super().form_valid(form)
#
#     def get_form(self, form_class=None):
#         self.object = super().get_form(form_class)
#         return self.object
#
#     def get_success_url(self):
#         return reverse('shop:product_list')


class ViewUserPasswordReset(PasswordResetView):
    template_name = 'account/reset/password_reset_form.html'
    email_template_name = 'account/reset/password_reset_email.html'
    success_url = reverse_lazy('account:reset_done')
    form_class = UserPasswordResetForm


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
