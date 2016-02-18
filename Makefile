# Makefile - use this file for all project-related actions

SCRIPTS = utils/scripts
GUNICORN_PID = gunicorn.pid


# travis auto-merge. Use ONLY with Travis
auto-merge:
	cd utils/scripts && ./auto-merge.sh

# install requirements in system (no virtualenv)
install_requirements_no_vnenv:
	pip install -r utils/requirements_back.txt

# run all tests using manage.py default server and no venv (everything installed in the system)
test_no_venv:
	export DEBUG=False ; python manage.py migrate ; python manage.py runserver & python manage.py test ; pkill python

# run app with gunicorn server
run_gunicorn:
	$(SCRIPTS)/run_gunicorn.sh $(GUNICORN_PID)

# stop app runned with gunicorn
stop_gunicorn:
	$(SCRIPTS)/stop_gunicorn.sh $(GUNICORN_PID)

# run app with manage runserver
run_manage:
	$(SCRIPTS)/run_manage.sh

# stop app runned with manage runserver
stop_manage:
	pkill python

# install system packages and basic app
install_basic:
	make install_system_packages
	make install_app

# install app after installing system packages
install_app:
	$(SCRIPTS)/install_app.sh

# install system packages that require sudo privileges
install_system_packages:
	sudo $(SCRIPTS)/install_system_packages.sh
