Schedule Creation
=================

This documentation is incomplete.

Creating a Schedule object
--------------------------

The first part of the schedule that needs to be created is the `Schedule`
object.

  - One `Schedule` should be created per session. For an example of this, see
    the `London 2016 schedule`_ (which consists of one day of tutorial sessions,
    and two days of general sessions).
  - The "Published" checkbox should be unchecked. Otherwise, the schedule
    will appear to be the public while it is being created.
  - Make sure that the dates in this object correspond with the dates of the
    schedule.
  - For readability, the names of `slot kinds` should not correspond to room
    names. If a presentation does not appear in a slot on the schedule, the
    name of the slot kind will appear by default.

.. _London 2016 schedule: https://pydata.org/london2016/schedule/

Creating Rooms
--------------

The name of the room will appear on the schedule at the top of each column.
Rooms are associated with Schedules, so conferences with multiple sessions
might have duplicates.

Adding Presentations to the Schedule
------------------------------------

`Presentation` objects are automatically created when a `Proposal` is accepted.

*to be written*

Adding Plenary Sessions
+++++++++++++++++++++++

Plenary sessions that do not have associated `Presentations` (e.g.
"Registration") are added directly as slots. In order to ensure that they
contain the correct content, the "Content overrride" field must be filled out.

*to be written*
