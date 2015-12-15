### Sistema de Pruebas e Integración Continua

El proyecto está basado en Django, por lo tanto hace uso del sistema de prueba de código que ofrece el framework Django. Para más información, ver [Django tests](https://docs.djangoproject.com/en/1.8/topics/testing/). Para pasar las pruebas en local, he creado un fichero [**Makefile**](https://github.com/gabriel-stan/gestion-tfg/blob/master/Makefile). Basta con ejecutar la orden **make test** para pasar las pruebas.

![make test](https://www.dropbox.com/s/0521o5vf5ijip08/maketest.png?dl=1)

Para poder automatizar el proceso de pruebas y desarrollar el proyecto bajo el concepto de Desarrollo Basado en Pruebas e Integración Continua, el proyecto está integrado con  las plataformas [Travis-CI](https://travis-ci.org/) y [Shippable](https://app.shippable.com/), ya que ofrecen posibilidades de despliegue automatizado en plataformas como [Docker](https://www.docker.com/) o [Heroku](https://www.heroku.com/). La configuración se indica en un fichero [**".yml"**](https://github.com/gabriel-stan/gestion-tfg/blob/master/.travis.yml).

Pasando pruebas en Travis:

![travis](https://www.dropbox.com/s/ocglq7ft3l2oczp/travis.png?dl=1)

Pasando pruebas en Shippable:

![shippable](https://www.dropbox.com/s/mioc1q32qxi9jlt/shippable.png?dl=1)

Tanto Travis como Shippable funcionan con el mismo fichero .yml, por tanto no es necesario crear varios ficheros de confi	guración para el testeo de la aplicacion. No obstante, si se requieren diferentes configuraciones, se tiene que añadir un fichero "shippable.yml" con la nueva configuración requerida. 
