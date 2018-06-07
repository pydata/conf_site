from django.conf import settings
from django.contrib.auth import get_user_model, hashers
from django.core.urlresolvers import reverse

from conf_site.accounts.tests import AccountsTestCase


PASSWORD_MISMATCH_ERROR_MESSAGE = "You must type the same password each time."
PASSWORD_WRONG_ERROR_MESSAGE = "Please type your current password."
FIELD_REQUIRED_ERROR_MESSAGE = "This field is required."


class PasswordChangeTestCase(AccountsTestCase):
    def test_anonymous_password_change_view(self):
        """Verify that anon users redirect to password reset view."""
        response = self.client.get(reverse("account_password"))
        self.assertRedirects(
            response=response,
            expected_url=reverse("account_password_reset"),
        )

    def test_password_change_view(self):
        """Verify that password change view displays when logged in."""
        # The force_login method is quicker and this isn't where
        # we test whether logging in works successfully.
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_password"))
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response,
            text="Change my password",
            status_code=200,
        )

    def test_no_password_change_without_current_password(self):
        """Verify change failure when not entering current password."""
        self.client.force_login(self.user)
        password_data = {
            "password_current": "",
            "password_new": "qwerty",
            "password_new_confirm": "qwerty",
        }
        response = self.client.post(reverse("account_password"), password_data)
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
            "password_current": "this is not my current password",
            "password_new": "this is my new password",
            "password_new_confirm": "this is my new password",
        }
        response = self.client.post(reverse("account_password"), password_data)
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
            "password_current": self.password,
            "password_new": "this is a new password",
            "password_new_confirm": "",
        }
        response = self.client.post(reverse("account_password"), password_data)
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
            "password_current": self.password,
            "password_new": "this is a new password",
            "password_new_confirm": "this is a different new password",
        }
        response = self.client.post(reverse("account_password"), password_data)
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertContains(
            response=response,
            text=PASSWORD_MISMATCH_ERROR_MESSAGE,
            status_code=200,
        )

    def test_successful_password_change(self):
        """Verify change success when entering password properly."""
        new_password = "this is my new password"

        self.client.force_login(self.user)
        password_data = {
            "password_current": self.password,
            "password_new": new_password,
            "password_new_confirm": new_password,
        }
        response = self.client.post(reverse("account_password"), password_data)
        # User should be redirected if there are no form errors.
        self.assertRedirects(
            response=response,
            expected_url=reverse(
                settings.ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL),
        )
        # Verify that user's new password was set correctly.
        # Re-retrieve user so that we can access new password.
        user = get_user_model().objects.get(email=self.user.email)
        assert(hashers.check_password(new_password, user.password))
