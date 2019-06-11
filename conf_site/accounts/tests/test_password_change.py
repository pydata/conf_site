from factory import fuzzy

from django.contrib.auth import get_user_model, hashers
from django.urls import reverse

from conf_site.accounts.tests import AccountsTestCase


PASSWORD_MISMATCH_ERROR_MESSAGE = "You must type the same password each time."
PASSWORD_WRONG_ERROR_MESSAGE = "Please type your current password."
FIELD_REQUIRED_ERROR_MESSAGE = "This field is required."


class PasswordChangeTestCase(AccountsTestCase):
    def setUp(self):
        super(PasswordChangeTestCase, self).setUp()
        self.new_password = fuzzy.FuzzyText(length=16)

    def test_password_change_view(self):
        """Verify that password change view displays when logged in."""
        # The force_login method is quicker and this isn't where
        # we test whether logging in works successfully.
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_change_password"))
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response, text="Change my password", status_code=200
        )

    def test_no_password_change_without_current_password(self):
        """Verify change failure when not entering current password."""
        self.client.force_login(self.user)
        password_data = {
            "oldpassword": "",
            "password1": self.new_password,
            "password2": self.new_password,
        }
        response = self.client.post(
            reverse("account_change_password"), password_data
        )
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response,
            text=FIELD_REQUIRED_ERROR_MESSAGE,
            status_code=200,
        )

    def test_no_password_change_with_invalid_current_password(self):
        """Verify change failure when entering invalid current password."""
        self.client.force_login(self.user)
        password_data = {
            "oldpassword": "this is not my current password",
            "password1": self.new_password,
            "password2": self.new_password,
        }
        response = self.client.post(
            reverse("account_change_password"), password_data
        )
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response,
            text=PASSWORD_WRONG_ERROR_MESSAGE,
            status_code=200,
        )

    def test_no_password_change_confirmation(self):
        """Verify change failure when not confirming your password."""
        self.client.force_login(self.user)
        password_data = {
            "oldpassword": self.password,
            "password1": self.new_password,
            "password2": "",
        }
        response = self.client.post(
            reverse("account_change_password"), password_data
        )
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response,
            text=FIELD_REQUIRED_ERROR_MESSAGE,
            status_code=200,
        )

    def test_invalid_password_change_confirmation(self):
        """Verify change failure when entering two different passwords."""
        self.client.force_login(self.user)
        password_data = {
            "oldpassword": self.password,
            "password1": self.new_password,
            "password2": "this is a different new password",
        }
        response = self.client.post(
            reverse("account_change_password"), password_data
        )
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response,
            text=PASSWORD_MISMATCH_ERROR_MESSAGE,
            status_code=200,
        )

    def test_successful_password_change(self):
        """Verify change success when entering password properly."""
        self.client.force_login(self.user)
        password_data = {
            "oldpassword": self.password,
            "password1": self.new_password,
            "password2": self.new_password,
        }
        response = self.client.post(
            reverse("account_change_password"), password_data
        )
        # User should be redirected if there are no form errors.
        self.assertRedirects(
            response=response, expected_url=reverse("account_change_password")
        )
        # Verify that user's new password was set correctly.
        # Re-retrieve user so that we can access new password.
        user = get_user_model().objects.get(email=self.user.email)
        assert hashers.check_password(self.new_password, user.password)
