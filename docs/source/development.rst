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

  - libffi-dev
  - libpq-dev
  - libpython-dev
  - pip
  - virtualenv
  - virtualenvwrapper

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
