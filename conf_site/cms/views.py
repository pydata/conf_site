from django.template.response import TemplateResponse

from account.forms import LoginEmailForm
from account.views import LoginView


def csrf_failure(request, reason=""):
    """
    Custom view for users who encounter CSRF errors.

    https://docs.djangoproject.com/en/1.9/ref/settings/#csrf-failure-view

    When we upgrade to Django 1.10, this view can be removed.

    """
    response = TemplateResponse(
        request=request, template="403_csrf.html", status=403)
    return response


class LoginEmailView(LoginView):
    """Custom login view that uses django-user-account's email form."""
    form_class = LoginEmailForm
