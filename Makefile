install-requirements:
	pip install -r requirements.txt

test:
	cd gestion_tfg && python manage.py test && gunicorn gestion_tfg.wsgi --log-file -
