from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


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
    image_credit = RichTextField(blank=True, default="")
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
        MultiFieldPanel(
            [
                ImageChooserPanel("background_image"),
                FieldPanel("image_credit"),
            ],
            heading="Banner Image",
        ),
        StreamFieldPanel("conference_info_section"),
        StreamFieldPanel("pydata_info_section"),
        StreamFieldPanel("news_keynote_section"),
        MultiFieldPanel(
            [
                FieldPanel("ticketing_section"),
                FieldPanel("ticketing_url"),
            ],
            heading="Ticketing",
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel("footer1_section"),
                FieldPanel("footer_email"),
                FieldPanel("footer_twitter"),
            ],
            heading="Footer",
        ),
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
    image_credit = RichTextField(blank=True, default="")
    venue_info_section = StreamField(
        HTMLBlock(required=False),
        blank=True,
        help_text=("Information about the conference's venue."))
    google_maps_url = models.URLField(blank=True, max_length=2083)
    hotel_info_section = StreamField(
        HTMLBlock(required=False),
        blank=True,
        help_text=("Information about the conference's hotel(s)."))

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel("background_image"),
                FieldPanel("image_credit"),
            ],
            heading="Banner Image",
        ),
        StreamFieldPanel("venue_info_section"),
        FieldPanel("google_maps_url"),
        StreamFieldPanel("hotel_info_section"),
    ]
