from django.core.urlresolvers import reverse

from rest_framework import status

from conf_site.api.tests import ConferenceSiteAPITestCase


class ConferenceSiteAPIConferenceTestCase(ConferenceSiteAPITestCase):
    def test_conference_api_anonymous_user(self):
        response = self.client.get(reverse("conference-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "title": self.CONFERENCE_TITLE,
            "start_date": self.CONFERENCE_START,
            "end_date": self.CONFERENCE_END,
        })
