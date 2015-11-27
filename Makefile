install-requirements:
	pip install -r requirements.txt

test:
	echo $TRAVIS_BRANCH
	cd gestion_tfg && python manage.py test
