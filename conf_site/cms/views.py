from account.forms import LoginEmailForm
from account.views import LoginView


class LoginEmailView(LoginView):
    """Custom login view that uses django-user-account's email form."""
    form_class = LoginEmailForm
