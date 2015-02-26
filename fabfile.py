import os

from fabric.api import cd, env, local, require, run, sudo, task


@task
def production():
    """ User production server settings """
    env.hosts = ['conf.pydata.org']
    env.project_root = '/www/conf_site'
    env.code_root = os.path.join(env.project_root, 'source')
    env.environment = 'production'
    env.forward_agent = True


@task
def update_requirements():
    """ update external dependencies on remote host """
    require('project_root')
    requirements = os.path.join(env.code_root, 'requirements')
    cmd = ['{0}/env/bin/pip install -q'.format(env.project_root)]
    cmd += ['--requirement %s' % os.path.join(requirements, 'base.txt')]
    run(' '.join(cmd))


@task
def manage_run(command):
    """
    Run a Django management command on the remote server.
    """
    require('environment')
    # Setup the call
    settings = 'conf_site.settings.{0}'.format(env.environment)
    manage_sh = u"DJANGO_SETTINGS_MODULE={0} /www/conf_site/manage.sh ".format(settings)
    sudo(manage_sh + command)


@task
def manage_shell():
    manage_run('shell')


@task
def deploy():
    require('code_root')
    with cd(env.code_root):
        run('git pull')
    update_requirements()
    manage_run('syncdb')
    manage_run('migrate')
    manage_run('collectstatic --noinput')
    # TBD restart nginx


@task
def collectstatic():
    manage_run('collectstatic --noinput')


@task
def ssh():
    require('hosts')
    local('ssh {0}'.format(env.hosts[0]))
