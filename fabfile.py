"""
You must specify the target environment by prefacing tasks
with `vagrant` or `production`. For example, to run collectstatic
in a production environment::

    fab production collectstatic

Notes:

The first time you deploy a site, run the `loadfixtures` task, but do not
run it repeatedly as it is not idempotent.

"""
import os

from fabric.api import (
    cd,
    env,
    local,
    require,
    sudo,
    task,
)
from fabric.contrib import files as ffiles
import fabtools
from fabtools.files import upload_template
from fabtools import supervisor
from fabtools.require import (
    deb,
    files,
    nginx,
    postgres,
)

# fabric settings
env.forward_agent = True
env.use_ssh_config = True
# project settings
env.fab_home = os.path.dirname(os.path.abspath(__file__))
env.deploy_dir = os.path.join(env.fab_home, 'deploy')
env.managed = "This file is managed by Fabric. Do not edit"
env.project_root = '/www/conf_site'
env.code_root = os.path.join(env.project_root, 'source')
env.virtualenv = os.path.join(env.project_root, 'env')
env.repo = 'https://github.com/pydata/conf_site.git'
env.webuser = 'seattle2015'
env.nginx_config = 'seattle2015-site.conf.j2'


@task
def seattle():
    """ Use production. Preface tasks with production to run in production. """
    env.environment = 'production'
    env.hosts = ['seattle.pydata.org']
    env.server_name = 'seattle.pydata.org'
    env.requirements = 'production.txt'
    env.webuser = 'seattle2015'
    env.nginx_config = 'seattle2015-site.conf.j2'


@task
def london():
    """ Use production. Preface tasks with production to run in production. """
    env.environment = 'production'
    env.hosts = ['london.pydata.org']
    env.server_name = 'london.pydata.org'
    env.requirements = 'production.txt'
    env.webuser = 'london2015'
    env.nginx_config = 'london2015-site.conf.j2'

@task
def nyc():
    """ Use production. Preface tasks with production to run in production. """
    env.environment = 'production'
    env.hosts = ['172.99.67.21']
    env.server_name = 'nyc.pydata.org'
    env.requirements = 'production.txt'
    env.webuser = 'nyc2015'
    env.nginx_config = 'nyc2015-site.conf.j2'

@task
def vagrant():
    """ Use vagrant. Preface tasks with vagrant to run in vagrant. """
    vc = get_vagrant_config()
    env.user = vc['user']
    env.hosts = vc['hosts']
    env.key_filename = vc['key_filename']
    env.forward_agent = vc['forward_agent']
    env.environment = 'vagrant'
    env.server_name = ''
    env.requirements = 'vagrant.txt'

@task
def uname():
    require('environment')
    sudo('uname -a')

@task
def deploy(version='master'):
    """ Deploys site

    version: a git reference. defaults to master.
    environment: defaults to production. preface with 'vagrant' to deploy to vagrant.
    """
    require('environment')
    setup_user()
    update_system_dependencies()
    deploy_files(version)
    setup_database()
    require_virtualenv()
    update_requirements()
    migrate()
    collectstatic()
    deploy_nginx()
    deploy_supervisor()

@task
def manage(command, environment="production"):
    """
    Run a Django management command on the remote server.
    """
    require('virtualenv', 'environment', 'code_root', 'webuser')
    manage_cmd = '{virtualenv}/bin/django-admin.py {command} --settings=conf_site.settings.{module} --pythonpath={code_root}'.format(**{
        'command': command,
        'virtualenv': env.virtualenv,
        'module': env.environment,
        'code_root': env.code_root,
    })
    with cd(env.code_root):
        sudo(manage_cmd, user=env.webuser)

@task
def loadfixtures():
    """ load default fixtures. warning: this is not idempotent!
    """
    require('environment')
    manage('loaddata fixtures/*')

@task
def shell_plus():
    """ Run a Django shell on the remote server """
    require('environment')
    manage('shell_plus')

@task
def migrate():
    """ Run a Django migration on the remote server """
    require('environment')
    manage('migrate')

@task
def collectstatic():
    """ Run a Django collectstatic command on the remote server """
    require('environment')
    manage('collectstatic --noinput')
    sudo('chmod -R a+rx %s' % os.path.join(env.code_root, 'public'))

@task
def ssh():
    """ ssh to the remote site
    """
    require('environment', 'hosts')
    local('ssh {0}'.format(env.hosts[0]))

@task
def restart_supervisor():
    require('environment')
    supervisor.restart_process('gunicorn')

@task
def restart_nginx():
    require('environment')
    sudo('service nginx restart')


def deploy_files(version='master'):
    """
    Ensure that the directory tree exists and has the requested
    version of the site.

    """
    require('code_root', 'project_root', 'repo', 'webuser')

    files.directory(env.project_root, owner=env.webuser, use_sudo=True)
    files.directory(
        os.path.join(env.project_root, 'log'),
        owner=env.webuser,
        use_sudo=True)
    if env.environment != "vagrant" and not ffiles.exists(env.code_root):
        with cd(env.project_root):
            sudo('git clone {} source'.format(env.repo), user=env.webuser)
    files.file(
        os.path.join(env.code_root, 'conf_site/settings/secrets.py'),
        source=os.path.join(env.deploy_dir, 'secrets.py'),
        use_sudo=True,
        owner=env.webuser)
    if env.environment != "vagrant":
        with cd(env.code_root):
            # discard any local changes to the repo
            sudo('git reset --hard', user=env.webuser)
            sudo('git checkout {}'.format(version), user=env.webuser)
            sudo('git pull', user=env.webuser)


def deploy_nginx():
    """ ensure that nginx is installed and our site is enabled """
    require('managed', 'server_name')
    nginx.server()
    upload_template(
        env.nginx_config,
        '/etc/nginx/sites-available/%s.conf' % env.webuser,
        context={
            'server_name': env.server_name,
            'managed': env.managed,

        },
        use_jinja=True,
        use_sudo=True,
        template_dir=env.deploy_dir,
    )
    nginx.enabled('%s.conf' % env.webuser)
    nginx.disabled('default')
    restart_nginx()


def deploy_supervisor():
    """ ensure that our supervisor is configured and enabled """
    require('environment')
    django_settings = 'DJANGO_SETTINGS_MODULE="conf_site.settings.{}"'.format(env.environment)
    fabtools.require.supervisor.process(
        'gunicorn',
        command='/www/conf_site/env/bin/gunicorn conf_site.wsgi:application --bind=0.0.0.0:8001 --workers=3 --timeout=180',
        directory='/www/conf_site/source',
        user=env.webuser,
        stdout_logfile='/www/conf_site/log/gunicorn.log',
        redirect_stderr=True,
        stderr_logfile='/www/conf_site/log/gunicorn.error.log',
        autostart=True,
        autorestart=True,
        stopasgroup=True,
        killasgroup=True,
        stopwaitsecs=60,
        environment=django_settings,
    )
    supervisor.update_config()
    restart_supervisor()

def update_system_dependencies():
    deb.uptodate_index(max_age={'hour': 1})
    deb.packages([
        'python-software-properties',
        'build-essential',
        'python-dev',
        'python-pip',
        'python-virtualenv',
        'postgresql',
        'postgresql-server-dev-9.3',
        'nginx',
        'libxml2',
        'libxml2-dev',
        'libxslt1-dev',
        'libxslt-dev',
        'supervisor',
        'libjpeg-dev',
        'libtiff-dev',
        'zlib1g-dev',
        'git',
        # not required but nice to have
        'tig',
        'tmux',
        'htop',
        'ack-grep',
    ])

def update_requirements():
    """ update external dependencies on remote host """
    require('virtualenv', 'requirements', 'code_root', 'webuser')
    requirements = os.path.join(env.code_root, 'requirements')
    cmd = ['{0}/bin/pip install -q'.format(env.virtualenv)]
    cmd += ['--requirement %s' % os.path.join(requirements, env.requirements)]
    sudo(' '.join(cmd), user=env.webuser)

def require_virtualenv():
    """ create virtualenv if it does not exist """
    require('virtualenv', 'webuser')
    if not ffiles.exists(env.virtualenv):
        sudo('virtualenv {}'.format(env.virtualenv), user=env.webuser)

def setup_user():
    """ creates the user that will run the website.
    """
    require('webuser')
    if env.environment == "vagrant":
        # This is not required for Vagrant because the user is created during `vagrant up`.
        return

    if not fabtools.user.exists(env.webuser):
        sudo('useradd {}'.format(env.webuser))

def setup_database():
    require('webuser')
    postgres.server()
    if not postgres.user_exists(env.webuser):
        sudo('createuser -S -D -R -w {}'.format(env.webuser), user='postgres')
    if not postgres.database_exists(env.webuser):
        postgres.database(env.webuser, env.webuser, encoding='UTF8', locale='en_US.UTF-8')

def get_vagrant_config():
    """
    Parses vagrant configuration and returns it as dict of ssh parameters
    and their values so that we can update the fabric environment when
    deploying to vagrant.
    """
    result = local('vagrant ssh-config', capture=True)
    conf = {}
    for line in iter(result.splitlines()):
        parts = line.split()
        conf[parts[0]] = ' '.join(parts[1:])
    vc = {
        'user': conf['User'],
        'hosts': ['%s:%s' % (conf['HostName'], conf['Port'])],
        'key_filename': conf['IdentityFile'].strip('"'),
        'forward_agent': conf.get('ForwardAgent', 'no') == 'yes',
        'environment': 'vagrant',
        'requirements': 'vagrant.txt',
        'server_name': '',
    }
    return vc
