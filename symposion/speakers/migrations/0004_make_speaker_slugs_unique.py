from django.db import migrations
from django.utils.text import slugify

import autoslug.fields
from autoslug.utils import generate_unique_slug


def create_default_slugs_for_speakers(apps, schema_editor):
    Speaker = apps.get_model("symposion_speakers", "Speaker")
    for speaker in Speaker.objects.all():
        speaker.slug = generate_unique_slug(
            Speaker._meta.get_field("slug"),
            speaker,
            slugify(speaker.name),
            None,
        )
        speaker.save()


class Migration(migrations.Migration):

    dependencies = [("symposion_speakers", "0003_speaker_slug")]

    operations = [
        migrations.RunPython(create_default_slugs_for_speakers),
        migrations.AlterField(
            model_name="speaker",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default="",
                editable=True,
                help_text=(
                    "Slug that appears in speaker URLs. "
                    "Automatically generated from the speaker's name. "
                    "This field should not be edited after the "
                    "schedule has been published."
                ),
                max_length=100,
                populate_from="name",
                unique=True,
            ),
        ),
    ]
