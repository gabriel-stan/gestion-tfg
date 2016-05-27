# Makefile - use this file for all project-related actions

SCRIPTS = utils/scripts
GUNICORN_PID = gunicorn.pid
RUN_ENV = ~/gestfg/run_env
INSTALL_ENV = ~/gestfg/install_env
REQUIREMENTS_BACK = utils/requirements_back.txt
REQUIREMENTS_BACK = utils/requirements_front.txt


##############
##  Travis  ##
##############

# travis auto-merge. Use ONLY with Travis
auto-merge:
	cd utils/scripts && ./auto-merge.sh

###############
##  testing  ##
###############

# run all tests using manage.py default server and no venv (everything installed in the system)
test_no_venv:
	export DEBUG=False ; python manage.py makemigrations ; python manage.py migrate ; python manage.py test

###################
##  app control  ##
###################

# run app with gunicorn server
run_gunicorn:
	$(SCRIPTS)/run_gunicorn.sh $(GUNICORN_PID) $(RUN_ENV)

# stop app runned with gunicorn
stop_gunicorn:
	$(SCRIPTS)/stop_gunicorn.sh $(GUNICORN_PID)

# run app with manage runserver
run_manage:
	$(SCRIPTS)/run_manage.sh $(RUN_ENV)

# stop app runned with manage runserver
stop_manage:
	pkill python

###############
##  install  ##
###############

# install requirements in system (no virtualenv)
install_requirements_no_vnenv:
	pip install -r utils/requirements_back.txt
	pip install -r utils/requirements_front.txt
	make install_postgres

# install system packages and basic app
install_basic:
	make install_system_packages
	make install_app

# install app after installing system packages
install_app:
	$(SCRIPTS)/install_app.sh $(REQUIREMENTS_BACK) $(REQUIREMENTS_FRONT)

# install system packages that require sudo privileges
install_system_packages:
	sudo $(SCRIPTS)/install_system_packages.sh

# install postgres
install_postgres:
	./$(SCRIPTS)/postgres.sh