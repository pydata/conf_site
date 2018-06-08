from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class HTMLBlock(StreamBlock):
    raw_html = RawHTMLBlock()
    rich_text = RichTextBlock()


# This class previously had a custom get_context method. It has
# been retained to make future customizations easier.
class CustomPage(Page):
    class Meta:
        abstract = True


class HTMLPage(CustomPage):
    """General page model containing blocks of HTML content."""
    content = StreamField(HTMLBlock())

    content_panels = Page.content_panels + [StreamFieldPanel("content"), ]


class HomePage(CustomPage):
    logo_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        help_text="Maximum file size is 10 MB",
        on_delete=models.SET_NULL,
        related_name="+"
    )
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        help_text="Maximum file size is 10 MB",
        on_delete=models.SET_NULL,
        related_name="+"
    )
    conference_info_section = StreamField(
        HTMLBlock(required=False),
        blank=True)
    pydata_info_section = StreamField(
        HTMLBlock(required=False),
        blank=True)
    news_keynote_section = StreamField(
        HTMLBlock(required=False),
        blank=True)
    ticketing_section = RichTextField(default="<h2>Tickets</h2>")
    ticketing_url = models.URLField(blank=True, max_length=2083)
    footer1_section = StreamField(
        HTMLBlock(required=False),
        blank=True,
        help_text=("Displays on left side of the site's footer section. "
                   "Will display mini code of conduct by default."))
    footer_email = models.EmailField(
        blank=True, default="admin@pydata.org", max_length=254)
    footer_twitter = models.CharField(
        blank=True, default="PyData", max_length=15)

    content_panels = Page.content_panels + [
        ImageChooserPanel("logo_image"),
        ImageChooserPanel("background_image"),
        StreamFieldPanel("conference_info_section"),
        StreamFieldPanel("pydata_info_section"),
        StreamFieldPanel("news_keynote_section"),
        FieldPanel("ticketing_section"),
        FieldPanel("ticketing_url"),
        StreamFieldPanel("footer1_section"),
        FieldPanel("footer_email"),
        FieldPanel("footer_twitter"),
    ]
    template = "homepage.html"


class VenuePage(CustomPage):
    """Page for venue and hotel information."""
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        help_text="Maximum file size is 10 MB",
        on_delete=models.SET_NULL,
        related_name="+"
    )
    venue_info_section = StreamField(HTMLBlock())
    google_maps_url = models.URLField(blank=True, max_length=2083)
    hotel_info_section = StreamField(HTMLBlock())

    content_panels = Page.content_panels + [
        ImageChooserPanel("background_image"),
        StreamFieldPanel("venue_info_section"),
        FieldPanel("google_maps_url"),
        StreamFieldPanel("hotel_info_section"),
    ]
