from django.db import migrations
from django.utils.text import slugify

import autoslug.fields
from autoslug.utils import generate_unique_slug


def create_default_slugs_for_presentations(apps, schema_editor):
    Presentation = apps.get_model("symposion_schedule", "Presentation")
    for presentation in Presentation.objects.all():
        presentation.slug = generate_unique_slug(
            Presentation._meta.get_field("slug"),
            presentation,
            slugify(presentation.title),
            None,
        )
        presentation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_schedule', '0002_presentation_slug'),
    ]

    operations = [
        migrations.RunPython(create_default_slugs_for_presentations),
        migrations.AlterField(
            model_name="presentation",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                default="",
                editable=True,
                help_text=(
                    "Slug that appears in presentation URLs. "
                    "Automatically generated from the presentation's title. "
                    "This field should not be edited after "
                    "the schedule has been published."
                ),
                max_length=100,
                populate_from="title",
                unique=True,
            ),
        )
    ]
