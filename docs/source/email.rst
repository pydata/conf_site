Email
=====

Conference sites send email for a variety of transactional reasons, including
email address confirmations, password resets, sponsorship applications and
proposal result notifications.

There are currently two possible ways to send email: SendGrid and SMTP.

SendGrid
--------

`SendGrid`_ is an external email service provider (ESP). Conference sites
integrate with SendGrid through the `sendgrid_django library`_. Setting the
Ansible variable ``sendgrid_api_key`` will automatically cause SendGrid to be
used in production environments.

.. _SendGrid: https://sendgrid.com/
.. _sendgrid_django library: https://github.com/elbuo8/sendgrid-django

SMTP
----

SMTP is the standard way to send email, but using it can cause deliverability
issues (especially when sending proposal result notifications).

Required Ansible variables:

  - ``email_host_name`` - the name of the SMTP server. This is pushed to
    Django's ``EMAIL_HOST`` setting.
  - ``email_host_user`` - the name of the SMTP server user. This is pushed
    to Django's ``EMAIL_HOST_USER`` setting.
  - ``email_host_password`` - the password used to access the SMTP server. This
    is pushed to Django's ``EMAIL_HOST_PASSWORD`` setting.


Other
-----

It is possible to use an email service provider other than SendGrid. The
easiest way is by using the provider's SMTP server. The difficulty of
integrating another provider is dependent on the configuration of the library
used for integration.
