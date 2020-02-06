from random import randint

from django.contrib.auth.models import Group

from conf_site.accounts.tests.factories import UserFactory
from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.reviews.views.export import ExportReviewersView


class ExportReviewersViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportReviewersView
    view_name = "reviewer_export"

    def setUp(self):
        super().setUp()

        self.reviewers_group = Group.objects.get_or_create(name="Reviewers")[0]

    def test_including_all_reviewers(self):
        reviewers = UserFactory.create_batch(size=randint(2, 4))
        for reviewer in reviewers:
            reviewer.groups.add(self.reviewers_group)
            reviewer.save()

        response = self.view_class().get()

        for reviewer in reviewers:
            self.assertContains(response, reviewer.id)
            self.assertContains(response, reviewer.get_full_name())
            self.assertContains(response, reviewer.email)

    def test_not_including_non_reviewers(self):
        users_not_reviewers = UserFactory.create_batch(size=randint(2, 4))

        response = self.view_class().get()

        for user in users_not_reviewers:
            self.assertNotContains(response, user.get_full_name())
            self.assertNotContains(response, user.email)
