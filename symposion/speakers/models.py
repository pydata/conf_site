from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

from autoslug.fields import AutoSlugField
from timezone_field import TimeZoneField

from symposion.markdown_parser import parse


class Speaker(models.Model):

    SESSION_COUNT_CHOICES = [(1, "One"), (2, "Two")]

    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="speaker_profile",
        verbose_name=_("User"),
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        help_text=_(
            "As you would like it to appear in the" " conference program."
        ),
    )
    slug = AutoSlugField(
        default="",
        editable=True,
        help_text=(
            "Slug that appears in speaker URLs. Automatically "
            "generated from the speaker's name. This field should "
            "not be edited after the schedule has been published."
        ),
        max_length=100,
        populate_from="name",
        unique=True,
    )
    biography = models.TextField(
        blank=True,
        help_text=_(
            "A little bit about you.  Edit using "
            "<a href='https://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
        ),
        verbose_name=_("Biography"),
    )
    biography_html = models.TextField(blank=True)
    time_zone = TimeZoneField(verbose_name=_("Timezone"))
    photo = models.ImageField(
        upload_to="speaker_photos",
        blank=True,
        help_text=_("Maximum file size: 10 MB"),
        verbose_name=_("Photo"),
    )
    github_username = models.CharField(
        max_length=39, blank=True, help_text=_("Your Github account")
    )
    twitter_username = models.CharField(
        max_length=15, blank=True, help_text=_("Your Twitter account")
    )
    linkedin_url = models.URLField(
        blank=True, max_length=2083, verbose_name="LinkedIn"
    )
    personal_url = models.URLField(
        blank=True, max_length=2083, verbose_name="Personal Site URL"
    )
    annotation = models.TextField(
        blank=True, verbose_name=_("Annotation")
    )  # staff only
    invite_email = models.CharField(
        blank=True,
        default="",
        max_length=200,
        db_index=True,
        verbose_name=_("Invite_email"),
    )
    invite_token = models.CharField(
        blank=True,
        max_length=40,
        db_index=True,
        verbose_name=_("Invite token"),
    )
    created = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name=_("Created")
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

    def save(self, *args, **kwargs):
        self.biography_html = parse(self.biography)
        return super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("speaker_edit")

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email

    @property
    def all_presentations(self):
        presentations = []
        if self.presentations:
            for p in self.presentations.all():
                presentations.append(p)
            for p in self.copresentations.all():
                presentations.append(p)
        return presentations

    @property
    def not_cancelled_presentations(self):
        """Property containing non-cancelled presentations."""
        presentations = []
        if self.presentations:
            for p in self.presentations.exclude(cancelled=True):
                presentations.append(p)
            for p in self.copresentations.exclude(cancelled=True):
                presentations.append(p)
        return presentations
