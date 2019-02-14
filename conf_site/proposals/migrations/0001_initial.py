# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_proposals', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('proposalbase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='symposion_proposals.ProposalBase')),
                ('audience_level', models.IntegerField(choices=[(1, 'Novice'), (3, 'Intermediate'), (2, 'Experienced')])),
                ('recording_release', models.BooleanField(default=True, help_text='By submitting your proposal, you agree to give permission to the conference organizers to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box.')),
            ],
            options={
            },
            bases=('symposion_proposals.proposalbase',),
        ),
    ]
