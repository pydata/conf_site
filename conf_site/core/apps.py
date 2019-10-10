from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        import conf_site.core.wagtail_hooks              # noqa: F401
