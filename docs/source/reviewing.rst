Reviewing Proposals
===================

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

Reviewers can send messages to proposal submitters in order to clarify
details of their proposals. Anonymity is dependant on the type of reviewing
system.

Voting
------

There are four different voting options:

  - +1 — **Good proposal and I will argue for it to be accepted**.
  - +0 — **OK proposal, but I will not argue for it to be accepted**.
  - −0 — **Weak proposal, but I will not argue against acceptance**.
  - −1 — **Serious issues and I will argue to reject this proposal**.

Commenting
~~~~~~~~~~

Reviewers can add comments when voting to provide additional information
or details to other reviewers.


.. _reviewing-creating-presentations:

Creating Presentations
----------------------

Presentations can be created by clicking the "Create Presentations"
button on the list of accepted proposals. A proposal must be accepted
before a presentation can be created for it.

Notification Process
--------------------

Email messages can be sent to selected proposal submitters by using the
"Send Email Message" section below the list of proposals.
