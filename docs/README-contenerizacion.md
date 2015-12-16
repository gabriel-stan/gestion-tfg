### Entorno de Pruebas

[**Docker**](https://www.docker.com/) permite crear entornos aislados mediante virtualización del SO, llamados contenedores. Estos contenedores se pueden usar como entornos aislados de pruebas o entornos de despliegue. Estos contenedores se ejecutan a partir de una imagen.

Para la creación de la imagen se ha utilizado un fichero `Dockerfile`. El contenido del fichero es el siguiente:
```
# Sistema Operativo
FROM ubuntu:latest

# Autor
MAINTAINER Gabriel Stan

# Preparacion del contenedor
RUN sudo apt-get update
RUN sudo apt-get install -y git
RUN sudo apt-get install -y build-essential

# Descarga del repositorio y preparacion de la aplicacion
RUN git clone https://github.com/gabriel-stan/gestion-tfg.git

RUN cd gestion-tfg && make run-docker

# Comando para lanzar la aplicacion
CMD cd gestion-tfg && make run
```

Ver el fichero Dockerfile [aquí](../Dockerfile).

La imagen contiene todo lo necesario para ejecutar la aplicación. Hay disponible una imagen actualizada constantemente desde el repositorio de Github a través de un `automated build`. La imagen está disponible [aquí](https://hub.docker.com/r/gabrielstan/gestion-tfg/) y se puede descargar mediante la orden `sudo docker pull gabrielstan/gestion-tfg:latest`. En el repositorio también hay disponible una versión de la imagen según el estado de desarrollo del proyecto (development).

Para probar la aplicación en un entorno local basta con ejecutar el comando `make install-docker`, el cual se asegurará de tener instalado Docker en el sistema, descargará la imagen de DockerHub y ejecutará la aplicación en un contenedor.

Una vez ejecutada, la aplicación se puede acceder a través del enlace `<ip-contenedor>:8000`.


