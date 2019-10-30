Deployment
==========

Initial Deployment and Creation
-------------------------------

It is assumed that each conference site will run on its own virtual private
server (VPS) running `Debian 9 (Stretch)`_. PyData uses Rackspace, but other
VPS providers like DigitalOcean_, Linode_, or `Amazon Lightsail`_ should also
be acceptable.

The user account on the server should have passwordless sudo access.

.. _Debian 9 (Stretch): https://wiki.debian.org/DebianStretch
.. _DigitalOcean: https://www.digitalocean.com/
.. _Linode: https://www.linode.com/
.. _Amazon Lightsail: https://amazonlightsail.com/

Suggested Minimum VPS Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 1 VCPU/CPU core
- 1 GB RAM
- 20 GB HDD/SSD space

The Host Variables file
~~~~~~~~~~~~~~~~~~~~~~~

Once a virtual server is set up, information related to the conference
should be added into an Ansible host variables file. This file should be
placed in the `ansible/host_vars` directory. The `conf_site` repository
contains `an example file`_ that might be helpful.

.. note::
   Many of these host variables are overridden in local development by
   group variables defined in `ansible/group_vars/development`.

Suggested variables in this file include:

- **ansible_ssh_host**: The IP address of the virtual server.
- **conference_identifier**: An alphanumeric string identifying the conference.
- **conference_name**: The title of the conference.
- **database_user**: The name of the PostgreSQL database user that will be
  created during deployment. For PyData sites, this is the
  `conference_identifer`.
- **django_database**: The name of the PostgreSQL database that will be
  created during deployment. For PyData sites, this is generally the
  `conference_identifer`.
- **google_analytics_id**: A valid `Google Analytics tracking ID`_.
- **subdirectory**: By default, this is the same as the `conference_identifier`
  (with a preceding slash).
- **time_format**: A string in `Django date/time templating format`_
  explaining how times should be formatted on the conference site.
  American sites use "`g:i A`", while European sites use "`G:i`".
- **timezone**: The conference site's timezone. This should be in
  `tz database format`_.
- **website_domain**: The domain where the conference site is located. For
  PyData sites, this should always be *pydata.org*.
- **website_url**: The full URL of the conference site. For PyData sites, this
  should be a subdirectory of pydata.org.

.. warning::
   It is assumed that conference sites are in a subdirectory of
   another website, connecting through a `reverse proxy`_. If this is not the
   case, modifications will need to be made to the nginx server configuration
   file templates in the `ansible/roles/web/templates/` directory so that
   the conference site will load properly.

.. _an example file: https://github.com/pydata/conf_site/blob/master/ansible/host_vars/example
.. _Google Analytics tracking ID: https://support.google.com/analytics/answer/1032385
.. _Django date/time templating format: https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#date
.. _tz database format: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
.. _reverse proxy: https://en.wikipedia.org/wiki/Reverse_proxy

Updating the Host Inventory
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ensure that code is deployed to the aforementioned VPS, its name
needs to be added to the Ansible hosts file (located at `ansible/hosts`_).

For PyData sites, a listing with the conference identifier should be added
to the `production` group. For other sites, the entire `production` group
should be replaced with your own server(s).

.. _ansible/hosts: https://github.com/pydata/conf_site/blob/master/ansible/hosts

The Secrets File
~~~~~~~~~~~~~~~~

The repository includes an encrypted `Ansible Vault`_ file at
`ansible/secrets.yml` containing sensitive variables that cannot
be included in plaintext. Non-PyData users should replace this file with
their own variables file. An example of the file and its format can
be found at `ansible/secrets.yml.example`.

.. _Ansible Vault: https://docs.ansible.com/ansible/playbooks_vault.html

Required variables include:

- **amy_password**: A password for an administrative user account.
- **database_password**: The PostgreSQL database password.
- **django_secret_key**: The `Django SECRET_KEY setting`_.
- **email_host_name**: The hostname of the SMTP server that sends email
  from the conference site.
- **email_host_password**: The password of the SMTP server. The username
  is defined in the Jinja template file for sensitive settings at
  `ansible/roles/web/templates/sensitive-settings.py` (`EMAIL_HOST_USER`).
- **upstream_server_ip**: The upstream server working as a reverse proxy
  for this conference website.

.. _Django SECRET_KEY setting: https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-SECRET_KEY

Deploying
~~~~~~~~~

Deployment occurs by running the `ansible-playbook` command::

    ansible-playbook ansible/production.yml -l gotham2017,metropolis2017

.. warning::
   Make sure that your virtualenv is activated (`workon conf_site`)
   before trying to deploy.

.. note::
   The optional `-l` parameter limits the deployment to a specific host
   or group of hosts.

Customization
-------------

There are a number of steps to get a new conference site ready. Most of these
steps are not necessary to be run manually for PyData conference sites.

- **Create additional Django administrator accounts if necessary.** The
  easiest way to do this is to login with the master admin account
  (using the admin email address defined in `ansible\group_vars\all` and
  the admin password defined in the Ansible Vault file) in the Wagtail admin
  (in the `cms` subfolder of the conference site's URL) and `adding users`_.
- **Create a new root page** using the HomePage model
  (see :ref:`wagtail-page-types`) to replace the default "Welcome to Wagtail"
  page.
- **Update the default Wagtail Site** with the correct name and the
  new root page. This can be found in the "Settings" menu.
- **Delete or unpublish the "Welcome to Wagtail" page**.
- **Load fixtures to help set up sites.** While the data in these fixtures
  are specific to PyData sites, it is a good idea for other users to edit
  and run them as well to `avoid possible issues`_. If not using Ansible,
  you need to manually login to the server, navigate to the application
  directory, activate the current virtualenv, and run the Django
  management command to load fixtures::

    ssh <conference site IP address>
    cd /srv/pydata
    source ~/.virtualenvs/current/bin/activate
    DJANGO_SETTINGS_MODULE="conf_site.settings.production" ./manage.py loaddata fixtures/*

- **Add a banner image** (required), appropriate text sections (recommended),
  Mailchimp list ID (optional, but necessary to have the mailing list
  subscription section show up), and ticketing website URL (optional,
  but enables ticketing links in the main menu and footer) to the homepage.
- **Manually create any additional pages**.
- **Add a main menu** in the "Settings" menu of the Wagtail admin. Only
  top-level menu items need to be added. *All pages that need to appear in the
  menu must have the "Show in menus" settings enabled* (found on the
  "Promote" tab when editing a page).
- **Update the conference name in the Django admin**.
- **Change the name of the Django Site in the Django admin**.
- **Open the Symposion proposal sections** if the call for proposals is
  already open. Change "Closed" to "No" in
  `admin/symposion_proposals/proposalsection/`.

.. _adding users: http://docs.wagtail.io/en/v1.9/editor_manual/administrator_tasks/managing_users.html
.. _avoid possible issues: https://github.com/pinax/symposion/pull/13
