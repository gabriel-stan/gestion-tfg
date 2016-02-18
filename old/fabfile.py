from fabric.api import run, local, hosts, cd, prefix
from fabric.contrib import django

#host info
def info():
    run('uname -s')


#check
def check():
	run('curl http://localhost:80/')


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
		run('cd gestion-tfg/ && pip install -r requirements.txt')
		run('cd gestion-tfg/gestion_tfg/ && python manage.py syncdb --noinput')
		run('cd gestion-tfg/gestion_tfg/ && python manage.py migrate')
		run('cd gestion-tfg/gestion_tfg/ && python manage.py makemigrations')


#run app
def run_app2():	
	with prefix('source gestion-tfg/venv/bin/activate'):
		run('cd gestion-tfg/gestion_tfg && sudo ../venv/bin/python manage.py runserver 0.0.0.0:80')

#run app
def run_app():
	with prefix('source gestion-tfg/venv/bin/activate'):
		run('cd gestion-tfg/ && make run')

#run app
def run_app3():
	run('cd gestion-tfg/ && sudo make runserver')
	#run('make runserver')


#install app
def install():

	install_packages()

	download_sources()

	install_environment()

	prepare_app()

	run_app3()

	check()

#delete_sources
def delete_sources():
	run('rm -rf gestion-tfg/')


def update_sources():
	run('cd gestion-tfg/ && git pull origin master')

def update_app():
	
	update_sources()

	prepare_app()



def download_docker():
	run('sudo apt-get update')
	run('sudo apt-get install -y docker.io')

def pull_docker():
	run('sudo docker pull hugobarzano/osl-computer-management:computer-management')

def run_docker():
	run('sudo docker run -i -t hugobarzano/osl-computer-management:computer-management')

def install_docker():
	download_docker()
	pull_docker()
	run_docker()
	