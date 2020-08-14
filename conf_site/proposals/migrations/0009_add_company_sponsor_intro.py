# Generated by Django 3.0.7 on 2020-07-02 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_add_mentoring_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='company_sponsor_intro',
            field=models.BooleanField(choices=[(True, 'Yes, I can make an introduction'), (False, 'No')], default=False, verbose_name='Would your company be interested in sponsoring the event?'),
            preserve_default=False,
        ),
    ]