#GESTFG - Plataforma de Gestión y Evaluación de Trabajos de Fin de Grado y Master

[![Build Status](https://travis-ci.org/gabriel-stan/gestion-tfg.svg?branch=master)](https://travis-ci.org/gabriel-stan/gestion-tfg) [![Build Status](https://img.shields.io/shippable/562e58f31895ca44742123f9.svg)](https://app.shippable.com/projects/562e58f31895ca44742123f9)


Antonio Manuel Rodriguez Castro  
Gabriel Stan

### Introducción

GESTFG es un sistema de gestión de los Trabajos de Fin de Grado y Master, que se va a usar inicialmente en la Escuela Técnica Superior de Ingenierías Informática y Telecomunicaciones de Granada, y posteriormente se podrá integrar en el resto de las Facultades de la Universidad de Granada o cualquier otra universidad. El proyecto en sí es el Trabajo de fin de Grado de los dos alumnos mencionados.

### Herramientas de desarrollo

Para el desarrollo de la plataforma se usará el framework Django. La plataforma será capaz de gestionar toda la información relacionada con los TFGs, gestión de usuarios, gestión de las diferentes fases (asignación, evaluación), interacción entre los miembros asignados a un TFG (alumnos, tutores y tribunal), notificaciones vía correo electrónico, evaluación de los TFG etc.

### Infraestructura Virtual

La plataforma tendrá un despliegue en **Microsoft Azure**, tal y como se detalla a continuación. Posteriormente se podrá configurar para un despliegue automatizado en cualquier infraestructura virtual.

**Frontend:** Una interfaz web en la que se reflejará toda la información relacionada con los TFG.  Se usará un servidor web en Microsoft Azure para procesar las peticiones de los usuarios a la interfaz web. 

**Backend:** Los servicios de la plataforma serán gestionados por el framework Django, y se repartirán (posiblemente) entre los frameworks Django y Tornado, para una mejor modularización y reparto de las funcionalidades de la plataforma.

**Gestión de bases de datos:** Se usará una base de datos SQL en Azure para guardar la información relacionada con los proyectos y posiblemente otra base de datos para guardar los datos más sensibles (relacionados con la evaluación etc), además se usará un sistema de backup de las BD posiblemente en otro proveedor cloud (BlueMix de IBM).

**Gestión de almacenamiento:** Se usará un servidor ftp en Azure Cloud Storage para guardar los archivos relacionados con los TFGs.

**Servidor de correo:** Se usará un servidor de correo para las notificaciones de eventos a los usuarios de la plataforma.

**Integración continua:** El proyecto se desarrollará dentro del concepto de DevOps, usando los servicios que ofrece Travis CI para una integración continua y un desarrollo basado en pruebas, asegurando la completa funcionalidad de la plataforma y un fácil mantenimiento.

**Backup:** Se realizará un servicio de replicación de la BD de forma automática configurando un servidor esclavo que será un espejo del servidor maestro utilizando postgreSQL (posiblemente).

**Balanceador de carga:** Para el balanceo de carga, se utilizará Nginx, se utilizará también para la carga de ficheros estáticos, cuyo tamaño puede ralentizar el sitio web.

**Seguridad:** 
- El objetivo será ofrecer las funcionalidades del sistema según el nivel de privilegios que tengan los diferentes usuarios, no pudiendo acceder a información si no tiene los permisos necesarios, asegurando la integridad y privacidad de los datos.  
- Los accesos de los usuarios serán ofrecidos por el departamento encargado de la gestión de la base de datos de usuarios de la universidad, por lo tanto nuestro sistema tratara con la información suministrada por ellos, no se manejan contraseñas.
- Los datos de la evaluación de los proyectos (en caso de ser almacenados) serán guardados junto con la información más confidencial del sistema (cuentas y posibles datos de los usuarios).


El  proyecto se ha presentado al certamen de proyectos de la [Oficina de Software Libre](http://osl.ugr.es/).


### Sistema de Pruebas e Integración Continua

El proyecto está basado en Django, por lo tanto hace uso del sistema de prueba de código que ofrece el framework Django. Para más información, ver [Django tests](https://docs.djangoproject.com/en/1.8/topics/testing/). Para pasar las pruebas en local, he creado un fichero [**Makefile**](https://github.com/gabriel-stan/gestion-tfg/blob/master/Makefile). Basta con ejecutar la orden **make test** para pasar las pruebas.

![make test](https://www.dropbox.com/s/0521o5vf5ijip08/maketest.png?dl=1)

Para poder automatizar el proceso de pruebas y desarrollar el proyecto bajo el concepto de Desarrollo Basado en Pruebas e Integración Continua, el proyecto está integrado con  las plataformas [Travis-CI](https://travis-ci.org/) y [Shippable](https://app.shippable.com/), ya que ofrecen posibilidades de despliegue automatizado en plataformas como [Docker](https://www.docker.com/) o [Heroku](https://www.heroku.com/). La configuración se indica en un fichero [**".yml"**](https://github.com/gabriel-stan/gestion-tfg/blob/master/.travis.yml).

Pasando pruebas en Travis:

![travis](https://www.dropbox.com/s/ocglq7ft3l2oczp/travis.png?dl=1)

Pasando pruebas en Shippable:

![shippable](https://www.dropbox.com/s/mioc1q32qxi9jlt/shippable.png?dl=1)

Tanto Travis como Shippable funcionan con el mismo fichero .yml, por tanto no es necesario crear varios ficheros de confi	guración para el testeo de la aplicacion. No obstante, si se requieren diferentes configuraciones, se tiene que añadir un fichero "shippable.yml" con la nueva configuración requerida. 

Para ver el avance del proyecto, revisar las ramas **BACKEND***, **FRONTEND*** y **dev**.

### Despliegue Continuo en un PaaS

Para facilitar el despliegue del proyecto, se va a usar [**Heroku**](https://www.heroku.com) como PaaS, un potente plataforma de despliegue continuo.

Ya que hacen falta ligeras modificaciones del proyecto y sus dependencias para poder desplegarlo en Heroku, he creado una nueva rama de despliegue, [deployment](https://github.com/gabriel-stan/gestion-tfg/tree/deployment), que va a contener la configuración de despliegue.

Para configurar Heroku, es necesario un fichero [Procfile](https://github.com/gabriel-stan/gestion-tfg/blob/deployment/Procfile) que contiene los comandos a ejecutar para poner en marcha el proyecto, una vez desplegado en Heroku.

Se pasa a configurar la app de Heroku, para enlazarla con el repositorio de GitHub. Cada vez que se detectan cambios en el repositorio y las pruebas de Integracion Continua pasan correctamente, Heroku procede a actualizar la aplicación ya deplegada.

![despliegue](https://www.dropbox.com/s/zgym6e943gm680g/herokugestfg.png?dl=1)

Para ver el avance del proyecto, revisar las ramas **BACKEND* **, **FRONTEND* ** y **dev**.

### Asignación de tareas

- Desarrollo: @tonimademo y @gabriel-stan
- Infraestructura Virtual: @gabriel-stan
