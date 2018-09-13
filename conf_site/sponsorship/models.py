from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon="group")
class SponsorshipSettings(BaseSetting):
    info_link = models.URLField(
        default=u"https://pydata.org/become-a-sponsor.html",
        max_length=2083,
        verbose_name=u"Link to information about becoming a sponsor.",
    )

    class Meta:
        verbose_name = u"sponsor settings"
