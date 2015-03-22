Deployment
==========

.. Note::
    Ideally we want to be able to deploy everything and run commands with Fabric.
    We cannot do this yet. Some manual steps are required.

    * A sysadm must create a user(s) and get authorized_keys in place for the user(s).
    * A sysadm must set up a DNS record for the site.

Fabric is used to deploy and manage the site.

fab production deploy
  This is the main command to use.
  This runs a deployment against the production server. This command will set
  up all of the services (postgresql, nginx, supervisor, gunicorn) needed to
  run the site, and will also update the source code and run some django 
  commands for you: migrate, collectstatic.

fab production manage:<cmd>
  This runs a django management command. The management command is passed to
  manage after the colon. The command needs to be quoted, e.g. "help shell"

fab production shell_plus
  This runs a django shell for you. It uses the enhanced shell from django-extensions.

fab production loadfixtures
  The first time you deploy the site you need to load up the fixtures to get starting content.

To list all of the available fabric tasks:: 

    fab -l

