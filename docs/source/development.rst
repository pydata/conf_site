Development
===========

Local Development
-----------------

This section assumes Vagrant_ and Virtualbox_ are installed.

.. _Vagrant: https://www.vagrantup.com/
.. _Virtualbox: https://www.virtualbox.org/

Use Vagrant and Virtualbox to create a local environment in a virtual machine
(VM) that matches production.::

    git clone https://github.com/pydata/conf_site.git
    cd conf_site
    vagrant up --provision

The main vagrant commands to use are:

vagrant up
  This starts up the VM. When you run it for the first time, it provisions the VM.

vagrant provision
  This deploys your current code to the VM.

vagrant halt
  When you aren't working on the project, you can turn off the VM with this command.

vagrant destroy
  This completely wipes away the VM. You can destroy it and start over.

vagrant ssh
  This logs you in to the VM as the vagrant user.
