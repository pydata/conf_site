from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField

from conf_site.cms.models import HTMLBlock


@register_setting(icon="date")
class ScheduleSettings(BaseSetting):
    legend = StreamField(
        HTMLBlock(required=False),
        blank=True,
        help_text="Text to appear on the schedule page.",
    )

    panels = [StreamFieldPanel("legend"), ]

    class Meta:
        verbose_name = u"schedule settings"
