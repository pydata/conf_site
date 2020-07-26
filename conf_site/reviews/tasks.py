import csv

from django.contrib.auth.models import Group, User

from allauth.account.models import EmailAddress
from allauth.utils import generate_unique_username


def import_reviewer_csv(filename):
    num_users_created = 0
    num_existing_users = 0
    with open(filename, "r", encoding="UTF-8-SIG") as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip header row.
        next(csvreader)

        for row in csvreader:
            try:
                first_name = row[1]
                last_name = row[2]
                email = row[3].lower()
            except IndexError:
                return False

            # Get an existing user account with the same email address.
            # If none exists, create a new user account with a username
            # generated from the first name or email address.
            if first_name:
                username = first_name
            else:
                username = email
            user, user_created = User.objects.get_or_create(
                email=email,
                defaults={"username": generate_unique_username([username])},
            )
            if user_created:
                num_users_created += 1
                EmailAddress.objects.create(user=user, email=email)
            else:
                num_existing_users += 1
            if not user.first_name:
                user.first_name = first_name
            if not user.last_name:
                user.last_name = last_name

            # Make sure user has reviewing permissions by adding
            # them to the right Group.
            reviewers_group = Group.objects.get(name="Reviewers")
            user.groups.add(reviewers_group)

            user.save()
    return (num_users_created, num_existing_users)
