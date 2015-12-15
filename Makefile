install-requirements:
	pip install -r requirements.txt

test:
	cd gestion_tfg && python manage.py test

auto-merge:
	./auto-merge.sh

install:
	./install.sh

run:
	./run.sh
