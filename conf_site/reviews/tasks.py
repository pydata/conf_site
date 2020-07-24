import csv

from django.contrib.auth.models import Group, User

from allauth.utils import generate_unique_username

from conf_site.proposals.models import Proposal
from conf_site.reviews.models import ProposalVote


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


def import_reviewer_proposal_matching_csv(filename):
    num_reviews_requested = 0
    warnings = []
    errors = []
    with open(filename, "r", encoding="UTF-8-SIG") as csvfile:
        csvreader = csv.reader(csvfile)
        # Skip header row.
        next(csvreader)

        for row in csvreader:
            try:
                reviewer_id = row[0]
                proposal_id = row[1]
            except IndexError:
                errors.append("Invalid row: {}".format(row))
                continue

            try:
                reviewer = User.objects.get(id=reviewer_id)
            except User.DoesNotExist:
                errors.append("User ID {} not found".format(reviewer_id))
                continue

            try:
                proposal = Proposal.objects.get(id=proposal_id)
            except Proposal.DoesNotExist:
                errors.append("Proposal ID {} not found".format(proposal_id))
                continue

            proposal_vote, vote_created = ProposalVote.objects.get_or_create(
                proposal=proposal, voter=reviewer
            )
            if not vote_created:
                warnings.append(
                    "Reviewer {} has already voted on proposal {}".format(
                        reviewer_id, proposal_id
                    )
                )
            else:
                num_reviews_requested += 1

        return {
            "num_reviews_requested": num_reviews_requested,
            "warnings": warnings,
            "errors": errors,
        }
