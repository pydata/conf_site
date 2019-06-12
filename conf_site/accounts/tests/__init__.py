from factory import fuzzy

from django.contrib.auth import get_user_model
from django.test import TestCase


class AccountsTestCase(TestCase):
    def setUp(self):
        super(AccountsTestCase, self).setUp()

        self.password = fuzzy.FuzzyText(length=16)
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
