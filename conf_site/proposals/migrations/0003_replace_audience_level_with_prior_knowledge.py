# Generated by Django 3.2.5 on 2021-07-07 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_add_under_represented_accessibility_sponsoring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='audience_level',
        ),
        migrations.AddField(
            model_name='proposal',
            name='prior_knowledge',
            field=models.CharField(choices=[('N', 'No previous knowledge expected'), ('Y', 'Previous knowledge expected')], default='N', max_length=1, verbose_name="Prior Knowledge"),
            preserve_default=False,
        ),
    ]