Conference Management
=====================

This site is built on a combination of Symposion_, a conference management
system and Wagtail_, a content management system. Most structured conference
data (e.g. proposals, speaker profiles, schedules) is located in Symposion
and be edited through the Django admin (located in the
``https://mysite/admin/`` directory), while most of the general content on
the site (e.g. the homepage's banner image, the text on the Venue page)
needs to be managed by Wagtail and its admin (located in the
``http://mysite/cms/`` directory).

.. _Symposion: https://symposion.readthedocs.io/en/latest/index.html
.. _Wagtail: http://docs.wagtail.io/en/latest/

Content Management
------------------

.. _wagtail-page-types:

Page Types
~~~~~~~~~~

There are three types of Wagtail pages that can be created.

- **HomePage** - a page containing specialized homepage data and sections.
  Each site should only have one of these.
- **VenuePage** - a page containing specialized information relating to the
  venue and hotel.
- **HTMLPage** - a generic page containing rich text and/or raw HTML.

Most of the pages you create should be HTMLPages.

Example: Creating a Call For Proposals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Goal
    :class: adminition note

    Create a Call for Proposals page

    For this example, we want to create a Call for Proposals on our
    site, at `https://mysite/cfp/`

Login to the Wagtail admin at ``https://mysite/cms/``. Navigate to the
root page - it should be the first page that appears when you click the
"Explorer" button in the left sidebar.

Wagtail should show the page as well as all of its child pages. Click
"Add a Child Page" and choose a `HTMLPage`. Edit the page and choose
`cfp` as its slug on the "Promote" tab.

You now have a *Call for Proposals* page at `https://mysite/cfp/`.

Main Menu
~~~~~~~~~

The main menu is managed from the "Settings" menu of the Wagtail admin. Only
top-level menu items need to be added. *All pages that need to appear in the
menu must have the "Show in menus" settings enabled* (found on the
"Promote" tab when editing a page).

Reviewing
---------

Teams
~~~~~

The reviewing section's permission structure relies on Symposion's "teams"
application.

Teams have three different types of membership status:

  - "open": Users can join freely.
  - "by application": Users can apply to join. Team managers receive
    email notification of applications and can approve applicants.
  - "by invitation": Users must be invited by a team manager in order
    to be able to join the team.

Each conference site should have a "Reviewers" team with the following
permissions for each conference section:

  - members need the `reviews || Can review ...` permission.
  - managers need the `reviews || Can manage ...` permission.
