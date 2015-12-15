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

La imagen se puede encontrar en [Docker Hub](https://hub.docker.com/r/gabrielstan/gestfg/) y se puede descargar con el comando `sudo docker pull gabrielstan/gestfg`. La imagen contiene todo lo necesario para ejecutar la aplicación.

Una vez ejecutada, la aplicación se puede acceder a través del enlace `<ip-contenedor>:8000`.

También está disponible una imagen actualizada constantemente desde el repositorio de Github a través de un `automated build`. La imagen está disponible [aquí](https://hub.docker.com/r/gabrielstan/gestion-tfg/).

Para probar la aplicación en un entorno local basta con ejecutar el comando `make install-docker`, el cual se asegurará de tener instalado Docker en el sistema, descargará la imagen de DockerHub y ejecutará la aplicación en un contenedor.


