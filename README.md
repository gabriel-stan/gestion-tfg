#GESTFG - Plataforma de Gestión y Evaluación de Trabajos de Fin de Grado y Master

[![Build Status](https://travis-ci.org/gabriel-stan/gestion-tfg.svg?branch=master)](https://travis-ci.org/gabriel-stan/gestion-tfg) [![Shippable](https://img.shields.io/shippable/562e58f31895ca44742123f9.svg)](https://app.shippable.com/projects/562e58f31895ca44742123f9) [![Heroku](https://heroku-badge.herokuapp.com/?app=gestfg&style=flat)](http://gestfg.herokuapp.com/) [![Deployment](https://img.shields.io/badge/deployment-deployed-brightgreen.svg)](http://gestfg.cloudapp.net/)



Antonio Manuel Rodriguez Castro  
Gabriel Stan

### Introducción

GESTFG es un sistema de gestión de los Trabajos de Fin de Grado y Master, que se va a usar inicialmente en la Escuela Técnica Superior de Ingenierías Informática y Telecomunicaciones de Granada, y posteriormente se podrá integrar en el resto de las Facultades de la Universidad de Granada o cualquier otra universidad. El proyecto en sí es el Trabajo de fin de Grado de los dos alumnos mencionados.


El  proyecto se ha presentado al certamen de proyectos de la [Oficina de Software Libre](http://osl.ugr.es/).

### Herramientas de desarrollo

Para el desarrollo de la plataforma se usará el framework Django. La plataforma será capaz de gestionar toda la información relacionada con los TFGs, gestión de usuarios, gestión de las diferentes fases (asignación, evaluación), interacción entre los miembros asignados a un TFG (alumnos, tutores y tribunal), notificaciones vía correo electrónico, evaluación de los TFG etc.

### Infraestructura Virtual

La plataforma tendrá un despliegue en [**Microsoft Azure**](https://azure.microsoft.com/es-es/) y/o [**Bluemix**](https://www.ibm.com/cloud-computing/bluemix/), tal y como se detalla a continuación. Posteriormente se podrá configurar para un despliegue automatizado en cualquier infraestructura virtual.

Más información [aquí](docs/README-infraestructura.md).


### Sistema de Pruebas e Integración Continua

El proyecto está basado en [**Django**](https://www.djangoproject.com/), por lo tanto hace uso del sistema de prueba de código que ofrece el framework Django. Para aprovechar al máximo un sistema de pruebas automatizado, el repositorio está enlazado con [**Travis CI**](https://travis-ci.org/).

Más información [aquí](docs/README-integracion-continua.md).

### Despliegue Continuo en un PaaS

Para facilitar el despliegue del proyecto, se va a usar [**Heroku**](https://www.heroku.com) como PaaS, una potente plataforma de despliegue continuo.

Más información [aquí](docs/README-despliegue-PaaS.md).

### Entorno de Pruebas

Para poder realizar pruebas fácilmente en un entorno totalmente aislado, se puede hacer uso de [**Docker**](https://www.docker.com/).

Más información [aquí](docs/README-contenerizacion.md).

### Despliegue Remoto con Fabric

Para poder desplegar y actualizar la aplciación remotamente, se puede hacer uso de la librería de python [Fabric](http://www.fabfile.org/).

Más información [aquí](docs/README-fabric.md).

### Despliegue en un IaaS con Vagrant

El proyecto está preparado para crear la infraestructura necesaria y ser desplegado en un entorno local o en [Azure](https://azure.microsoft.com/es-es/) con la ayuda de Vagrant. Para desplegar en Azure, sólo hay que modificar el fichero [env_vars.sh](env_vars.sh) y ejecutar el script [vagrant-azure.sh](vagrant-azure.sh), aparte de tener el entorno local preparado para el uso de [vagrant](https://www.vagrantup.com/) y [ansible](http://www.ansible.com/).

Más información [aquí](docs/README-vagrant.md).


### Asignación de tareas

- Desarrollo: @tonimademo y @gabriel-stan
- Infraestructura Virtual: @gabriel-stan
