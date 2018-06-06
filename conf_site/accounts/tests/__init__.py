from django.contrib.auth import get_user_model
from django.test import TestCase


class AccountsTestCase(TestCase):
    password = "hunter2"

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create(
            username="test",
            email="example@example.com",
            first_name="Test",
            last_name="User",
        )
        self.user.set_password(self.password)
        self.user.save()
