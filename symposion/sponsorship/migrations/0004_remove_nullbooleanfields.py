# Generated by Django 3.0.10 on 2020-12-31 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_sponsorship', '0003_language_updates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='company_description_benefit',
            field=models.BooleanField(help_text='Company description benefit is complete', null=True, verbose_name='Company description benefit'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='print_description_benefit',
            field=models.BooleanField(help_text='Print description benefit is complete', null=True, verbose_name='Print description benefit'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='print_logo_benefit',
            field=models.BooleanField(help_text='Print logo benefit is complete', null=True, verbose_name='Print logo benefit'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='web_logo_benefit',
            field=models.BooleanField(help_text='Web logo benefit is complete', null=True, verbose_name='Web logo benefit'),
        ),
        migrations.AlterField(
            model_name='sponsorbenefit',
            name='is_complete',
            field=models.BooleanField(help_text='True - benefit complete; False - benefit incomplete; Null - n/a', null=True, verbose_name='Complete?'),
        ),
    ]