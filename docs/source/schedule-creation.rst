Schedule Creation
=================

Creating a Schedule object
--------------------------

The first part of the schedule that needs to be created is the `Schedule`
object.

  - One `Schedule` should be created per session. For an example of this, see
    the `London 2016 schedule`_ (which consists of one day of
    tutorial sessions, and two days of general sessions).
  - The "Published" checkbox should be unchecked. Otherwise, the schedule
    will appear to be the public while it is being created.
  - Make sure that the dates in this object correspond with the dates of the
    schedule.

.. _London 2016 schedule: https://pydata.org/london2016/schedule/

Creating Rooms
--------------

The name of rooms will appear on the schedule at the top of each column.
`Rooms` are associated with `Schedules`, so a conference will multiple
sessions occurring in the same location will need multiple `Room` objects
with the same name.

Presentations
-------------

`Presentation` objects are automatically created when a `Proposal` is
accepted. Updating a presentation's proposal will automatically update the
presentation's information. Presentations that are attached to unaccepted
proposals will be deleted automatically by symposion.

Creating New Presentations
~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a new `Presentation` that will not be deleted automatically:

  - Create a new `User` for each speaker in the presentation.
  - Create a new `Speaker` attached to the aforementioned `Users`.
  - Create a new `Proposal`.
  - Create a new `Proposal Result` object attached to the
    aforementioned `Proposal`. Ensure that its status is "accepted".

Saving the `Proposal Result` will automatically create a `Presentation`
linked to the existing proposal.

Adding Presentations to a Schedule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Presentations` can most easily be added to a schedule by using the Django
admin to connect `Slots` to them. The slot's attributes (start time, end time,
and slot room) will determine where the presentation appears on the
schedule.

Adding a new `Slot` can be done directly from a `Presentation's` page in
the Django admin.

Modifying Presentations
~~~~~~~~~~~~~~~~~~~~~~~

Changing a `Presentation's` date or time is easily accomplished by editing
its slot.

Adding Plenary Sessions
-----------------------

Plenary sessions that do not have associated `Presentations` (e.g.
"Registration", "Lunch", etc.) are added directly as `Slots`. In order to
ensure that they contain the correct content, the "Content overrride"
field must be filled out.

Publishing
----------

Unpublished schedules are only visible to staff users. To make a schedule
publicly available, each `Schedule` object needs to have its "published"
attribute checked in the Django admin.
