from django.urls import reverse

from conf_site.accounts.tests import AccountsTestCase


INCORRECT_LOGIN_ERROR_MESSAGE = (
    "The email address and/or password you specified are not correct.")
FIELD_REQUIRED_ERROR_MESSAGE = "This field is required."


class UserLoginTestCase(AccountsTestCase):
    def test_login_view(self):
        """Verify that login view displays successfully."""
        response = self.client.get(reverse("account_login"))
        self.assertTemplateUsed(response, "account/login.html")
        self.assertContains(response=response, text="Log in", status_code=200)

    def test_login_with_wrong_email_address(self):
        """Verify that using an invalid email address fails."""
        login_data = {
            "email": "example2@example.com",
            "password": self.password,
        }
        response = self.client.post(reverse("account_login"), login_data)
        self.assertTemplateUsed(response, "account/login.html")
        self.assertContains(
            response=response,
            text=INCORRECT_LOGIN_ERROR_MESSAGE,
            status_code=200,
        )

    def test_login_with_no_password(self):
        """Verify that using no password fails."""
        login_data = {
            "email": self.user.email,
            "password": "",
        }
        response = self.client.post(reverse("account_login"), login_data)
        self.assertTemplateUsed(response, "account/login.html")
        self.assertContains(
            response=response,
            text=FIELD_REQUIRED_ERROR_MESSAGE,
            status_code=200,
        )

    def test_login_with_wrong_password(self):
        """Verify that using the wrong password fails."""
        login_data = {
            "email": self.user.email,
            "password": "42",
        }
        response = self.client.post(reverse("account_login"), login_data)
        self.assertTemplateUsed(response, "account/login.html")
        self.assertContains(
            response=response,
            text=INCORRECT_LOGIN_ERROR_MESSAGE,
            status_code=200,
        )

    def test_successful_login(self):
        """Verify that a correct email/password combination succeeds."""
        login_data = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(reverse("account_login"), login_data)
        self.assertRedirects(
            response=response,
            expected_url=reverse("dashboard"),
        )
