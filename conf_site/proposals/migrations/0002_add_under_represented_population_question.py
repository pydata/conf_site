# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='under_represented_population',
            field=models.BooleanField(
                default=False,
                help_text=b'Do you feel that you or your talk represent a '
                           'population under-represented in the Python '
                           'and/or Data community?'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='under_represented_short_answer',
            field=models.TextField(
                help_text=b'Additional information, if needed.', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='under_represented_short_answer_html',
            field=models.TextField(blank=True),
        ),
    ]
