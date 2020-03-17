from django.conf import settings


def core_context(self):
    """Context processor for elements appearing on every page."""
    context = {}
    context["jupytercon_base_url"] = settings.JUPYTERCON_BASE_URL
    context["google_analytics_id"] = settings.GOOGLE_ANALYTICS_PROPERTY_ID
    context["sentry_public_dsn"] = settings.SENTRY_PUBLIC_DSN
    return context
