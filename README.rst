
PyData Symposion
================


Below you will find basic setup and deployment instructions for the conference
website. These instructions assume you are using an Anaconda_ environment >= 3.8.

.. _Anaconda: http://docs.continuum.io/anaconda/install.html


Getting Started 
---------------

To setup your local conda environment::

    conda create --name conf_site pip python=2
    mkdir -p ~/anaconda/envs/conf_site/etc/conda/activate.d/
    echo "export DJANGO_SETTINGS_MODULE=conf_site.settings.local" > ~/anaconda/envs/conf_site/etc/conda/activate.d/django.sh
    mkdir -p ~/anaconda/envs/conf_site/etc/conda/deactivate.d/
    echo "unset DJANGO_SETTINGS_MODULE" > ~/anaconda/envs/conf_site/etc/conda/deactivate.d/django.sh

Activate the site::

    source activate conf_site

Install the necessary requirements::

    conda install pip
    pip install -r requirements/dev.txt

Local Development
-----------------

By default the local setup uses sqlite. To start off, first create the database::

    python manage.py migrate

Load the default fixtures for Symposion::

    python manage.py loaddata fixtures/*

You should now be able to run the development server::

    python manage.py runserver

Vagrant Development
-------------------

Use Vagrant combined with Fabric to get an environment locally that matches how
things are set up in production. You must have Vagrant installed for this to work::

    vagrant up
    fab vagrant deploy

By default this will check out the master branch of the repo on the vagrant box.

.. Note::
    It would be helpful to mount a local directory so that you can edit and run
    with local changes, but this is not ready yet. You can push work-in-progress
    to a branch as a workaround for now.


Deployment with Fabric
----------------------

The website is deployed via Fabric, and tasks are defined in the fabfile.py
Please see the comments in the fabfile.py to read more about how to use it.

To use Fabric with a VM, you need to have ssh credentials for that VM. When using
Vagrant this is handled for you.


Build Static Resources
----------------------

.. Warning:: 
    This section may not be accurate. Proceed with caution. I'm leaving this in from
    the first version of the README

By default, the project uses Bootstrap and LESS. The LESS files can be found in
``conf_site/static/conf_site/less``. When done editing your LESS files, you will
want to build the compiled CSS. Fortunately, there is a Makefile to assist in building
both JS and CSS resources. It is predicated on having NPM and a few related dependencies::

    sudo npm install -g uglify-js less
    cd conf_site/static/conf_site/
    make


