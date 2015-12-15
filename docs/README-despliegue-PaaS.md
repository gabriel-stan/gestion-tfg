### Despliegue Continuo en un PaaS

Para facilitar el despliegue del proyecto, se va a usar [**Heroku**](https://www.heroku.com) como PaaS, una potente plataforma de despliegue continuo.

Para configurar Heroku, es necesario un fichero [Procfile](https://github.com/gabriel-stan/gestion-tfg/blob/master/Procfile) que contiene los comandos a ejecutar para poner en marcha el proyecto, una vez desplegado en Heroku. Ademas, tambien se tiene que incluir un fichero [requirements.txt](https://github.com/gabriel-stan/gestion-tfg/blob/master/requirements.txt), para que se instalen las dependencias en el PaaS.

En Heroku se puede definir el despliegue automático desde GitHub, tal y como se muestra a continuacion. Cada vez que se detectan cambios en el repositorio y las pruebas de Integracion Continua pasan correctamente, Heroku procede a actualizar la aplicación ya desplegada.

![despliegue](https://www.dropbox.com/s/4pu112260c59i6l/deployfrommaster.png?dl=1)

Para la base de datos, Heroku ofrece un add-on **Heroku Postgres**, que es relativamente facil de configurar. 

![Postgres Heroku](https://www.dropbox.com/s/puhg1ddtpgus7wf/postgresheroku.png?dl=1)

Para ello, es necesario el paquete `dj-database-url`, incluido en el paquete `django-toolbelt`  que se puede instalar con el comando `pip install django-toolbelt`. En el entorno de despliegue, Heroku proporciona una variable `DATABASE_URL` que contiene los datos de conexion a la base de datos PostgreSQL. Para que Django pueda parsear la variable, simplemente se tiene que anadir en el fichero de configuracion de Django las siguientes lineas, tal y como se puede ver en el fichero [settings.py](https://github.com/gabriel-stan/gestion-tfg/blob/master/gestion_tfg/gestion_tfg/settings.py):

```python
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
```

Todo el proceso de configuracion y el despliegue a Heroku se puede hacer automaticamente ejecutando el script [deploy_to_heroku.sh](https://github.com/gabriel-stan/gestion-tfg/blob/master/deploy_to_heroku.sh), el cual contiene, entre otras cosas, lo siguente:

```bash
...
heroku create
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:wait
git add .
git push heroku master
heroku ps:scale web=1
```
El script va a crear un contenedor en Heroku, va a configurar la base de datos Postgres, va a desplegar la aplicacion y por ultimo va a ejecutar la aplicacion segun la configuracion del fichero [Procfile](https://github.com/gabriel-stan/gestion-tfg/blob/master/Procfile). Para ejecutar el script es necesario tener instalado [heroku toolbelt](https://toolbelt.heroku.com/).

Y por ultimo, la aplicacion de este repositorio se puede ver desplegada [**aqui**](http://gestfg.herokuapp.com/).