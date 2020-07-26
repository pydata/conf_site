import os
from shutil import copyfile
from tempfile import mkstemp

from django.contrib.auth.models import User

from allauth.account.models import EmailAddress

from conf_site.accounts.tests import AccountsTestCase
from conf_site.reviews.tasks import import_reviewer_csv
from conf_site.reviews.tests import ReviewingSuperuserMixin


class ImportReviewerCSVTestCase(ReviewingSuperuserMixin, AccountsTestCase):
    reverse_view_name = "reviewer_import"
    reverse_view_args = None

    def _temp_csv(self, csv_filename):
        """Wrapper function to move CSV to temporary file."""
        # Get complete file path, so that copyfile can find the file.
        csv_filepath = "{}/{}".format(
            os.path.realpath(os.path.dirname(__file__)), csv_filename
        )
        # The CSV file needs to be copied, because import_site_id_csv
        # will delete the file.
        temp_csv_filename = mkstemp(suffix=".csv")[1]
        copyfile(csv_filepath, temp_csv_filename)
        return temp_csv_filename

    def test_invalid_csv(self):
        """Test that a CSV file with invalid rows returns False."""
        num_initial_users = User.objects.count()
        csv_filename = self._temp_csv("invalid.csv")
        self.assertFalse(import_reviewer_csv(csv_filename))
        self.assertEqual(num_initial_users, User.objects.count())

    def test_not_importing_header_row(self):
        """Test that user number does not change if empty CSV is imported."""
        num_initial_users = User.objects.count()
        csv_filename = self._temp_csv("empty.csv")
        self.assertTrue(import_reviewer_csv(csv_filename))
        self.assertEqual(num_initial_users, User.objects.count())

    def test_using_test_csv(self):
        """Test that importing predefined CSV file works properly."""
        num_initial_users = User.objects.count()
        csv_filename = self._temp_csv("test.csv")
        self.assertTrue(import_reviewer_csv(csv_filename))
        # A single User should have been added.
        self.assertEqual(num_initial_users + 1, User.objects.count())
        # Verify that all user data/changes were properly imported.
        imported_user = User.objects.get(email="reviewer@example.com")
        self.assertTrue(imported_user.first_name, "Example")
        self.assertTrue(imported_user.last_name, "Reviewer")
        self.assertTrue(self.reviewers_group in imported_user.groups.all())
        EmailAddress.objects.get(email="reviewer@example.com")
