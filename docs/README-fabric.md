### Uso de Fabric

Con fabric se pueden ejecutar scripts de configuración remotamente en cualquier máquina virtual/servidor que tenga habilitado el acceso por ssh.

Es necesario tener instalado localmente el paquete `fabric`, que se puede instalar con el comando `sudo apt-get install fabric`.

A continuación, se puede ejecutar el comando `fab`. Para ello es necesario un fichero `fabfile.py`, localizado [aquí](../fabfile.py).

#### Despliegue de la aplicación.

Para desplegar la aplicación en la máquina remota es suficiente ejecutar el comando `fab -I -H host_name install`, el cual instalará dependencias, descargará las fuentes, preparará el entorno y ejecutará el servidor en el puerto 80.

#### Actualización de la aplicación.

Para actualizar la aplicación ya desplegada, es suficiente ejecutar el comando `fab -I -H host_name update_app`, el cual descargará las nuevas fuentes y aplicará las migraciones necesarias a la base de datos.

#### Despliegue actual

La aplicación está desplegada sobre una máquina virtual de Azure, y está disponible [aquí](http://gestfg.northeurope.cloudapp.azure.com). A continuación se muestra el proceso de despliegue.

Creación de la máquina virtual en azure:

![creacion](https://www.dropbox.com/s/zzn9kpinfwra37f/creacion_maquina.png?dl=1)

Comprobamos la conexión por ssh:

![connection](https://www.dropbox.com/s/nubjxp1ttj22jh6/conexion.png?dl=1)

![connection](https://www.dropbox.com/s/kxg1egff35pnpra/check_connection.png?dl=1)

Y por último, desplegamos la aplocación y comprobamos su funcionamiento con los comandos `fab -I -H gestfg@gestfg.northeurope.cloudapp.azure.com install` y `fab -I -H gestfg@gestfg.northeurope.cloudapp.azure.com check`. Debemos asegurarnos de que el puerto 80 está abierto en la máquina remota para poder acceder a la aplicación.

![despliegue](https://www.dropbox.com/s/3iiq8is2p84m8in/check_app.png?dl=1)


#### Despliegue con Docker

También se puede hacer uso de la imagen Docker, y se puede instalar la aplicación con el comando `fab -I -H host_name install_docker`.

