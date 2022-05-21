from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from website.celery import app


@app.task
def send_email_password_reset(subject_template_name, email_template_name, context,
                              from_email, to_email, html_email_template_name):
    context['user'] = User.objects.get(pk=context['user'])

    return PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
