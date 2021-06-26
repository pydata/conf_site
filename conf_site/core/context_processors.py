from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone

import pytz


def core_context(self):
    """Context processor for elements appearing on every page."""
    context = {}
    context["conference_title"] = Site.objects.get_current().name
    context["google_analytics_id"] = settings.GOOGLE_ANALYTICS_PROPERTY_ID
    context["sentry_public_dsn"] = settings.SENTRY_PUBLIC_DSN
    return context


def time_zone_context(self):
    context = {}
    # Duplicate the functionality of django.template.context_processors.tz.
    context["TIME_ZONE"] = timezone.get_current_timezone_name()
    # Add a list of time zones to the context.
    context["TIME_ZONES"] = pytz.common_timezones

    return context
