from datetime import datetime
import pytz

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


def synchronize_slot_time_fields(apps, schema_editor):
    Slot = apps.get_model("symposion_schedule", "Slot")
    for slot in Slot.objects.iterator():
        # Note that we assume that slot times should be associated
        # with the slot's Day and the application's current timezone.
        slot.start_dt = datetime(
            year=slot.day.date.year,
            month=slot.day.date.month,
            day=slot.day.date.day,
            hour=slot.start.hour,
            minute=slot.start.minute,
            second=slot.start.second,
            tzinfo=pytz.timezone(settings.TIME_ZONE),
        )
        slot.end_dt = datetime(
            year=slot.day.date.year,
            month=slot.day.date.month,
            day=slot.day.date.day,
            hour=slot.end.hour,
            minute=slot.end.minute,
            second=slot.end.second,
            tzinfo=pytz.timezone(settings.TIME_ZONE),
        )
        slot.save()


class Migration(migrations.Migration):

    dependencies = [
        ("symposion_schedule", "0003_make_presentation_slugs_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="slot",
            name="end_dt",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="End"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="slot",
            name="start_dt",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Start"
            ),
            preserve_default=False,
        ),
        migrations.RunPython(synchronize_slot_time_fields),
    ]
