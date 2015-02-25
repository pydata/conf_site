import os

from fabric.api import cd, env, local, require, run, sudo, task


@task
def production():
    """ User production server settings """
    env.hosts = ['conf.pydata.org']
    env.project_root = '/www/conf_site'
    env.code_root = os.path.join(env.project_root, 'source')
    env.environment = 'production'


@task
def update_requirements():
    """ update external dependencies on remote host """
    require('project_root')
    requirements = os.path.join(env.code_root, 'requirements')
    cmd = ['{0}/env/bin/pip install -q'.format(env.project_root)]
    cmd += ['--requirement %s' % os.path.join(requirements, 'base.txt')]
    run(' '.join(cmd))


@task
def deploy():
    require('code_root')
    with cd(env.code_root):
        run('git pull')
    update_requirements()
    with cd(env.project_root):
        run('{0}/env/bin/python manage.py syncdb --settings=conf_site.settings.{1}'.format(
            env.project_root, env.environment))
        run('{0}/env/bin/python manage.py migrate --settings=conf_site.settings.{1}'.format(
            env.project_root, env.environment))
        run('{0}/env/bin/python manage.py collectstatic --noinput --settings=conf_site.settings.{1}'.format(
            env.project_root, env.environment))
    sudo('/etc/init.d/apache2 restart')


@task
def manage(command):
    """
    Runs Django management commands
    """
    require('environment')
    with cd(env.project_root):
        run('{0}/bin/python manage.py {1} --settings=conf_site.settings.{2}'.format(
            env.code_root, command, env.environment))


@task
def ssh():
    require('hosts')
    local('ssh {0}'.format(env.hosts[0]))
