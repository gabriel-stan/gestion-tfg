from fabric.api import run, local, hosts, cd
from fabric.contrib import django

#host info
def info():
    run('uname -s')

#install app
def install():

	#install git
	run('sudo apt-get update')
	run('sudo apt-get install -y git')

	#download sources
	run('sudo git clone https://github.com/gabriel-stan/gestion-tfg')

	#install environment
	run('cd gestion-tfg/ && make install')

	#prepare app
	run('cd gestion-tfg/gestion_tfg/ && python manage.py syncdb --noinput')
	run('cd gestion-tfg/gestion_tfg/ && python manage.py migrate')
	run('cd gestion-tfg/gestion_tfg/ && python manage.py makemigrations')

	#run app
	run('cd gestion-tfg/ && make run')

#check
def check():
	run('curl http://localhost:8000/')
