======================
Reviewing in conf_site
======================

Permissions and Access Control
------------------------------

To review proposals, conference site users must be a member of the
"Reviewers" user group. Administrators (users with access to the conference
site's administration section) need to add users to this group in order for
them to have access.

Two dynamic settings (BLIND_AUTHORS and BLIND_REVIEWERS) determine whether the
type of reviewing system:

  - **single blind** - `BLIND_AUTHORS` is True and `BLIND_REVIEWERS` is False.
    Authors cannot see the identities of reviewers, but
    reviewers can see authors' identities.
  - **double blind** - both `BLIND_AUTHORS` and `BLIND_REVIEWERS` are True.
    Neither authors nor reviewers can see each others' identities.
  - **open** - both `BLIND_AUTHORS` and `BLIND_REVIEWERS` are False.
    Both authors and reviewers can see each others' identities.
  - **reverse blind** - `BLIND_AUTHORS` is False and `BLIND_REVIEWERS` is True.
    Authors can see reviewers' identities, but reviewers cannot see the
    identities of authors.

Single blind reviewing is the default. Like other dynamic settings,
BLIND_AUTHORS and BLIND_REVIEWERS can be modified from their defaults
by editing them on the Constance Config page in the Django admin.

Messaging
---------

Commenting
----------

Voting
------

Notification Process
--------------------
