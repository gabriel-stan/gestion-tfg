FROM ubuntu:latest
MAINTAINER Gabriel Stan

RUN sudo apt-get update
RUN sudo apt-get install -y git
RUN sudo apt-get install -y build-essential

RUN git clone https://github.com/gabriel-stan/gestion-tfg.git

RUN cd gestion-tfg && git checkout BACKEND-1

RUN cd gestion-tfg && make install

CMD cd gestion-tfg && make run