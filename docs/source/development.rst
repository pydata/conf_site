Development
===========

There are multiple ways you to prepare for development. This covers two examples.

Local Development
-----------------

This section assumes you have installed Anaconda_.

.. _Anaconda: http://docs.continuum.io/anaconda/install.html

Conda Environment
+++++++++++++++++

Set up a local conda environment::

    conda create --name conf_site pip python=2
    mkdir -p ~/anaconda/envs/conf_site/etc/conda/activate.d/
    echo "export DJANGO_SETTINGS_MODULE=conf_site.settings.local" > ~/anaconda/envs/conf_site/etc/conda/activate.d/django.sh
    mkdir -p ~/anaconda/envs/conf_site/etc/conda/deactivate.d/
    echo "unset DJANGO_SETTINGS_MODULE" > ~/anaconda/envs/conf_site/etc/conda/deactivate.d/django.sh

Activate the conda environment::

    source activate conf_site

Install the necessary requirements::

    conda install pip
    pip install -r requirements/dev.txt

Django Management
+++++++++++++++++

By default the local setup uses sqlite. To start off, first create the database::

    python manage.py migrate

Load the default fixtures for the site:: 

    python manage.py loaddata fixtures/*

At this point you can make changes and try them out with the development server::

    python manage.py runserver

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


Building Static Resources
-------------------------

.. Warning:: 
    This section is copied from the outdated README file and is not be accurate.
    Proceed with caution. It needs to be updated.

By default, the project uses Bootstrap and LESS. The LESS files can be found in
``conf_site/static/conf_site/less``. When done editing your LESS files, you will
want to build the compiled CSS. Fortunately, there is a Makefile to assist in building
both JS and CSS resources. It is predicated on having NPM and a few related dependencies::

    sudo npm install -g uglify-js less
    cd conf_site/static/conf_site/
    make

