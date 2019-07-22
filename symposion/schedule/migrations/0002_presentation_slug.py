from django.db import migrations

import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [("symposion_schedule", "0001_initial")]

    operations = [
        migrations.AddField(
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
            ),
        )
    ]
