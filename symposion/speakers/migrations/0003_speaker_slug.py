from django.db import migrations

import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [("symposion_speakers", "0002_standardize_markdown_links")]

    operations = [
        migrations.AddField(
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
            ),
        ),
    ]
