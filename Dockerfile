# Sistema Operativo
FROM ubuntu:latest

# Autor
MAINTAINER Gabriel Stan

# Preparacion del contenedor
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y build-essential

# Descarga del repositorio y preparacion de la aplicacion
RUN git clone https://github.com/gabriel-stan/gestion-tfg.git
RUN cd gestion-tfg && git checkout BACKEND-1

RUN cd gestion-tfg && make run-docker

# Comando para lanzar la aplicacion
CMD cd gestion-tfg && make run
