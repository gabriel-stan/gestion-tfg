from fabric.api import run, local, hosts, cd, prefix
from fabric.contrib import django

# usage: fab -i ssh_keyfile -H user@host --port=SSH_PORT action
# if there is a problem with SSH, update paramiko package with system pip

# host info
def info():
    run('uname -s')


# check
def check(port):
	run('curl http://localhost:'+port+'/')


# update sources
def update_sources():
	run('cd gestion-tfg && git pull')


# update app
def update_app():
    update_sources()
    run('cd gestion-tfg && make update_app')

# start server
def start_server():
    run('cd gestion-tfg && make run_gunicorn')

# restart server
def stop_server():
    run('cd gestion-tfg && make stop_gunicorn')

# restart server
def restart_server():
    run('cd gestion-tfg && make stop_gunicorn')
    run('cd gestion-tfg && make run_gunicorn')
