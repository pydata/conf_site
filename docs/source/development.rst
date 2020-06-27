Development
===========

Required Software
-----------------

Ansible_ is required to deploy conference site software to servers. For
local development, you will also need Vagrant_ and Virtualbox_ to manage the
virtual machine containing your development environment.

.. _Ansible: https://www.ansible.com/
.. _Vagrant: https://www.vagrantup.com/
.. _Virtualbox: https://www.virtualbox.org/

In order to successfully build virtualenvs, a number of development Python
libraries/packages should also be installed.

- python3-dev
- python3-pip
- python3-virtualenv
- libffi-dev
- libimagequant-dev
- libjpeg-dev
- libssl-dev
- libtiff-dev
- libxml2
- libxml2-dev
- libxslt-dev
- libxslt1-dev
- zlib1g-dev

Note that if you are not using a Debian server, the name of some of the
libraries may be different.

Local Development
-----------------

This section assumes all of the required software mentioned in the last
section has been installed successfully.

Use Vagrant and Virtualbox to create a local environment in a virtual machine
(VM) that matches production.::

    git clone https://github.com/pydata/conf_site.git
    cd conf_site
    mkvirtualenv conf_site
    vagrant up --provision

The main vagrant commands to use are:

vagrant up
  This starts up the VM. When you run it for the first time, it provisions the VM.

vagrant provision
  This uses Ansible to deploy your current code and other required settings to the VM.

vagrant halt
  When you aren't working on the project, you can turn off the VM with this command.

vagrant destroy
  This completely wipes away the VM. You can destroy it and start over.

vagrant ssh
  This logs you in to the VM as the vagrant user.


Walkthrough for OSX
-------------------

The following commands should get you a working setup on OSX for local development/testing.::

  $ brew cask install vagrant
  $ brew install ansible
  $ sudo /usr/bin/python3 -m pip install virtualenvwrapper
  $ export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
  $ virtualenvwrapper.sh conf_siteq
  $ ansible-vault create foo.yml
  # enter password and fill with content of ansible/secrets.yml.example
  $ cp foo.yml ansible/secrets
  $ vagrant up --provision

  # wait a few minutes
  $ vagrant ssh # this will connect to the VM or $ ssh -p2222 vagrant@127.0.0.1
  # Following https://github.com/pydata/conf_site/blob/b6df905f61ae37845387f31d02d959929aacf34f/docs/source/deployment.rst#customization
  # So the Following commands are inside the VM
  $ cd /srv/pydata
  $ source ~/.virtualenvs/current/bin/activate
  $ DJANGO_SETTINGS_MODULE="conf_site.settings.production" ./manage.py loaddata fixtures/*
  $ sudo systemctl start nginx
  # Now go to http://localhost:8080/test
  # and edit for instance templates/base.html
