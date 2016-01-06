from fabric.api import run, local, hosts, cd, prefix
from fabric.contrib import django

#host info
def info():
    run('uname -s')


#install packages
def install_packages():

	run('sudo apt-get update')
	run('sudo apt-get install -y git')
	run('sudo apt-get install -y make')


#download sources
def download_sources():

	run('git clone https://github.com/gabriel-stan/gestion-tfg')


#install environment
def  install_environment():
	run('cd gestion-tfg/ && make install')


#prepare app
def prepare_app():
	with prefix('source gestion-tfg/venv/bin/activate'):
		run('cd gestion-tfg/gestion_tfg/ && python manage.py syncdb --noinput')
		run('cd gestion-tfg/gestion_tfg/ && python manage.py migrate')
		run('cd gestion-tfg/gestion_tfg/ && python manage.py makemigrations')


#run app
def run_app2():	
	with prefix('source gestion-tfg/venv/bin/activate'):
		run('cd gestion-tfg/gestion_tfg && python manage.py runserver 0.0.0.0:8000')

#run app
def run_app():
	with prefix('source gestion-tfg/venv/bin/activate'):
		run('cd gestion-tfg/ && make runserver')


#install app
def install():

	install_packages()

	download_sources()

	install_environment()

	prepare_app()

	run_app()

#delete_sources
def delete_sources():
	run('rm -rf gestion-tfg/')

#check
def check():
	run('curl http://localhost:8000/')
