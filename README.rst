
PyData Symposion
========================

Below you will find basic setup and deployment instructions for the PyData Symposion Site
project. To begin you should have the following applications installed on your
local development system::

- Anaconda <http://docs.continuum.io/anaconda/install.html>
- git >= 1.7


Getting Started 
------------------------

To setup your local conda environment with the necessary requirements::

    conda create --name conf_site python=2
    pip install -r requirements/dev.txt

Export local Django settings to the conda environmnet::

    mkdir -p ~/anaconda/envs/conf_site/etc/conda/activate.d/
    echo "export DJANGO_SETTINGS_MODULE=conf_site.settings.local" > ~/anaconda/envs/conf_site/etc/conda/activate.d/django.sh

They should be unset during deacivation::

    mkdir -p ~/anaconda/envs/conf_site/etc/conda/deactivate.d/
    echo "unset DJANGO_SETTINGS_MODULE" > ~/anaconda/envs/conf_site/etc/conda/deactivate.d/django.sh

Activate the site::

    source activate conf_site

Create the Postgres database and run the initial syncdb/migrate::

    postgres -D /usr/local/var/postgres
    createdb -E UTF-8 conf_site
    python manage.py migrate

To load the default fixtures for Symposion::

    python manage.py loaddata fixtures/*

You should now be able to run the development server::

    python manage.py runserver


Build Static Resources
------------------------

By default, the project uses Bootstrap and LESS. The LESS files can be found in
``conf_site/static/conf_site/less``. When done editing your LESS files, you will
want to build the compiled CSS. Fortunately, there is a Makefile to assist in building
both JS and CSS resources. It is predicated on having NPM and a few related dependencies::

    sudo npm install -g uglify-js less
    cd conf_site/static/conf_site/
    make

Deployment
------------------------

You can deploy changes to a particular environment with
the ``deploy`` command::

    fab staging deploy

New requirements or migrations are detected by parsing the VCS changes and
will be installed/run automatically.
