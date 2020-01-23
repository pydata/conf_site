from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon="group")
class SponsorshipSettings(BaseSetting):
    info_link = models.URLField(
        default=u"https://pydata.org/pdf/sponsor-prospectus.pdf",
        max_length=2083,
        verbose_name=u"Link to sponsor prospectus.",
    )

    class Meta:
        verbose_name = u"sponsor settings"
