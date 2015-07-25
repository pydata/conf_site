Conference Management
=====================

This site is built on the Symposion_ conference management system.
Symposion has some basic docs that discuss its data models. It could
use more docs for the perspective of conference organizers.

This page is a start.

.. _Symposion: http://symposion.readthedocs.org/en/latest/index.html

Content Management
------------------

Content is managed by the Symposion CMS and Symposion Boxes apps.

Boxes
+++++

Boxes provide a wiki-like experience for edited small blocks of
text in sections of a page. The boxes app will present an *Edit this content*
link to edit a section of a page.

CMS Pages
+++++++++

Content is also stored at the page level by using the Symposion CMS app.
This app provides a wiki-like editor for an entire page rather than a section.

You can create a new page by navigating to a url path that does not yet exist.
The app will redirect you to an edit page where you can add and save content.

Example: Creating a Call For Proposals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Goal
    :class: adminition note

    Create a Call for Proposals page

    For this example, we want to create a Call for Proposals on our
    site, at `http://mysite/cfp/`

* In order to create the page, use your browser to nagivate to `http://mysite/cfp/`.
* Because this page does not exist yet, your browser is redirected to an edit page.
* In the *Title* field, type *Call for Proposals*
* In the *Body* text area, type the text for your CFP. *Proposals are now open!*
* Click the *Save* button.

You now have a *Call for Proposals* page at `http://mysite/cfp/` Now you can
add it to your *Site Tree* so that it appears in the navigation bar.

Site Tree
+++++++++

The Site-tree app creates navigation menus. These are edited in the Django
admin.

.. note:

    Our site-tree is created when the site is deployed. The starting contents
    are build from a fixture in the site's source code called sitetree.json

We have a sitetree called `main`.  You can view and edit the tree with the
*Site Trees* Django admin view.

Most of our site tree elements point to CMS Pages, and you can see this when
you view the tree and see url patterns such as *cms_page "cfp/"*.

.. admonition:: Goal
    :class: adminition note

    Add the Call for Proposals page as a top-level item in the navigation bar.

* Navigate to the Django admin page, `http://mysite/admin/`.
* Scroll to the *Site Trees* box and select the *Site Trees* element inside
  the box.
* From the resulting page, select *main*.
.. Warning:: 
    If *main* doesn't exist, stop! Something wrong happened when the site was
    deployed. Ask for help.
* When you select on this you will see a page that has a *Site Tree Items main*
  section.
* Select *Add Site Tree Item +*. This takes you to a new page.
* For this goal, we want to add the Call for Proposals page as a top-level
  item in the navaigation bar, so leave the *Parent:* option alone.
* Enter a title in the *Title* text field.
* In the *URL:* text field, type `cms_page "cfp/"`
* Ignore the *Access settings* section.
* In the *Display settings* section, Check the options that you
  want. For this example, be sure to select *Show in menu*.
* In the *Additional settings*, be sure that *URL as Pattern* is checked.
* Click *Save* to save the item.
* This will redirect you back to the *Change Site Tree* page for *main*. Don't
  forget to click *Save* on this page. If you forget, the Call for Proposals
  won't be added.

The django-sitetree_ app documents discuss in depth how to use the admin for
editing sitetree pages.

.. _django-sitetree: http://django-sitetree.readthedocs.org/en/latest/

.. Warning:: 
    The django admin might not show changes immediately on refresh.

Conference Committees
---------------------

TODO: add notes about the teams app.

Review Process
--------------

TODO: add notes about the review process.


Schedule Process
----------------

TODO: add notes about the schedule process.
