from factory import fuzzy

from django.contrib.auth import get_user_model
from django.test import TestCase


class AccountsTestCase(TestCase):
    def setUp(self):
        super(AccountsTestCase, self).setUp()

        self.password = str(fuzzy.FuzzyText(length=16))
        self.new_password = fuzzy.FuzzyText(length=16)

        user_model = get_user_model()
        self.user = user_model.objects.get_or_create(
            username="test",
            email="example@example.com",
            first_name="Test",
            last_name="User",
        )[0]
        self.user.set_password(self.password)
        self.user.save()

    def _become_staff(self):
        """Make this testcase's user a staff user."""
        self.user.is_staff = True
        self.user.is_superuser = False
        self.user.save()

    def _become_superuser(self):
        """Make this testcase's user a superuser."""
        self.user.is_superuser = True
        self.user.save()
