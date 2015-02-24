from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "conf_site"

    def ready(self):
        import_module("conf_site.receivers")
