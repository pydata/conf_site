Development
===========

Development with Vagrant
------------------------

This section assumes Vagrant_ is installed.

.. _Vagrant: http://docs.vagrantup.com/v2/installation/

Use Vagrant combined with Fabric to get an environment locally that matches how
things are set up in production.::

    git clone https://github.com/pydata/conf_site.git
    cd conf_site
    vagrant up
    fab vagrant deploy

Once you deploy the site, you can make changes locally and see them reflected 
on the deployed site. You may need to collectstatic and restart supervisor sometimes.
The fabfile has commands to do that.

* fab vagrant collectstatic
* fab vagrant restart_supervisor

The main vagrant commands to use are:

vagrant up
  This starts up the VM. When you run it for the first time, it provisions the VM.

vagrant halt
  When you aren't working on the project, you can turn off the VM with this command.

vagrant destroy
  This completely wipes away the VM. You can destroy it and start over.

vagrant ssh
  This logs you in to the VM as the vagrant user.
