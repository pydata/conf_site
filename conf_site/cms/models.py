from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page


class HTMLBlock(StreamBlock):
    raw_html = RawHTMLBlock()
    rich_text = RichTextBlock()


class CustomPage(Page):
    class Meta:
        abstract = True

    def get_context(self, request):
        """Pull additional context from homepage."""
        context = super(CustomPage, self).get_context(request)
        home_page = context['request'].site.root_page.specific
        context["mailchimp_list_id"] = home_page.mailchimp_list_id
        context["ticketing_url"] = home_page.ticketing_url
        return context


class HTMLPage(CustomPage):
    """General page model containing blocks of HTML content."""
    content = StreamField(HTMLBlock())

    content_panels = Page.content_panels + [StreamFieldPanel("content"), ]


class HomePage(CustomPage):
    logo_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    conference_info_section = StreamField(HTMLBlock())
    pydata_info_section = StreamField(HTMLBlock())
    ticketing_url = models.URLField(blank=True)
    mailchimp_list_id = models.CharField(blank=True, max_length=100)

    content_panels = Page.content_panels + [
        FieldPanel("logo_image"),
        FieldPanel("background_image"),
        StreamFieldPanel("conference_info_section"),
        StreamFieldPanel("pydata_info_section"),
        FieldPanel("ticketing_url"),
        FieldPanel("mailchimp_list_id"),
    ]
    template = "homepage.html"


class VenuePage(CustomPage):
    """Page for venue and hotel information."""
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    venue_info_section = StreamField(HTMLBlock())
    google_maps_url = models.URLField(blank=True)
    hotel_info_section = StreamField(HTMLBlock())

    content_panels = Page.content_panels + [
        FieldPanel("background_image"),
        StreamFieldPanel("venue_info_section"),
        FieldPanel("google_maps_url"),
        StreamFieldPanel("hotel_info_section"),
    ]
