install-requirements:
	pip install -r requirements.txt

test:
	cd gestion_tfg && python manage.py test

auto-merge:
	./auto-merge.sh

install-docker:
	./install_docker.sh

run-docker:
	./run_docker.sh

install:
	./install.sh

run:
	./run.sh

runserver:
	cd gestion_tfg/ && python manage.py runserver 0.0.0.0:8000 &
