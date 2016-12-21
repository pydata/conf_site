from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "conf_site"

    def ready(self):
        import_module("conf_site.receivers")
