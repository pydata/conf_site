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

Site Tree
+++++++++

Site-tree menus are handled by django-sitetree_. The django-sitetree documents
discuss in depth how to use the admin for editing sitetree pages.

.. _django-sitetree: http://django-sitetree.readthedocs.org/en/latest/

We have a sitetree that is loaded by the sitetree.json fixture when the site
is deployed. The fixture creates a sitetree called `main`. You can view the
tree with the *Site Trees* Django admin view.

Most of our site tree elements point to CMS Pages, and you can see this when
you view the tree and see url patterns such as *cms_page "about/mission/"*.

.. Warning:: 
    The django admin might not show changes immediately on refresh.

Conference Committees
---------------------

TODO: add notes about the teams app.

Review Process
--------------

TODO: add notes about the review process.
