# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a new user group named 'Reviewers'."

    def handle(self, *args, **options):
        group, group_created = Group.objects.get_or_create(name="Reviewers")
        if group_created:
            self.stdout.write("New 'Reviewers' user group was created.")
        else:
            self.stdout.write("'Reviewers' user group already existed.")
