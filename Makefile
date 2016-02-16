install-requirements:
	pip install -r requirements.txt

test:
	export DEBUG=False && python manage.py migrate && python manage.py runserver & python manage.py test && pkill python

auto-merge:
	./auto-merge.sh

install-docker:
	./install_docker.sh

run-docker:
	./run_docker.sh

install-packages:
	./install_packages.sh

install:
	./install.sh

run:
	./run.sh

runserver:
	cd gestion_tfg/ && sudo ../venv/bin/python manage.py runserver 0.0.0.0:80 &

deploy-azure:
	./vagrant-azure.sh

deploy-azure-norun:
	./vagrant-azure.sh norun
