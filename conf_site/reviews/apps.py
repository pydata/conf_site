from __future__ import unicode_literals

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = "conf_site.reviews"

    def ready(self):
        import conf_site.reviews.signals   # noqa: F401
