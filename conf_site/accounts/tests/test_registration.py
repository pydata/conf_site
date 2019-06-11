from factory import Faker, fuzzy

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserRegistrationTestCase(TestCase):
    def test_registration_view(self):
        """Verify that user registration view loads properly."""
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_user_registration(self):
        """Ensure that user registration works properly."""
        EMAIL = Faker("email").generate()
        PASSWORD = fuzzy.FuzzyText(length=16)
        test_user_data = {
            "password1": PASSWORD,
            "password2": PASSWORD,
            "email": EMAIL,
            "email2": EMAIL,
        }

        # Verify that POSTing user data to the registration view
        # succeeds / returns the right HTTP status code.
        response = self.client.post(
            reverse("account_signup"), test_user_data)
        # Successful form submission will cause the HTTP status code
        # to be "302 Found", not "200 OK".
        self.assertEqual(response.status_code, 302)

        # Verify that a User has been successfully created.
        user_model = get_user_model()
        user_model.objects.get(email=EMAIL)
