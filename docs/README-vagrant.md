### Despliegue en un IaaS

Para facilitar el despliegue y creación de la infraestructura necesaria, se hace uso de las herramientas [vagrant](https://www.vagrantup.com/) y [ansible](http://www.ansible.com/).

Requisitos:

- [ ] Ruby 2.0+
- [ ] Vagrant 1.6+
- [ ] VirtualBox 4.x (para un despliegue local)
- [ ] Ansible (herramienta de aprovisionamiento)
- [ ] Vagrant Plugin: vagrant-azure (para un despliegue en azure)
- [ ] Vagrant Plugin: vagrant-env (para las variables de entorno)

#### Despliegue local

Para un despliegue local, se puede usar el fichero [Vagrantfile_local.txt](../Vagrantfile_local.txt) renombrandolo a `Vagrantfile` y ejecutar el script [vagrant-local.sh](../vagrant-local.sh). Será necesario exportar una variable de entorno `VM_USER` o indicar el usuario en el [playbook.yml](../playbook.yml) de ansible. Recomendado usar `vagrant` como usuario para un despliegue local.

#### Despliegue en Azure

Requisitos:

- [ ] Generar y subir certificado al portal de administración de Azure
- [ ] Crear una cuenta de almacenamiento (storage) en azure, o de lo contrario desactivar la opción `azure.storage_acct_name` en el [Vagrantfile](../Vagrantfile).

Para generar el certificado se puede usar los siguientes comandos y subir el fichero `.cer`al portal de azure:

	openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout azure.pem -out azure.pem
	openssl x509 -inform pem -in azure.pem -outform der -out azure.cer
	chmod 600 azure.pem

Pasos a sequir para el despliegue en Azure (preparación del entorno local):

1. Instalar las dependencias indicadas anteriormente.
2. Rellenar las variables del fichero [env_vars.sh](../env_vars.sh) con la información de su cuenta azure y los datos de la máquina virtual a crear.
3. (Opcional) En el mismo fichero, modificar `ROOT_FOLDER` con el directorio que contiene el Vagrantfile y desde el cual se va a ejecutar el despliegue (normalmente `.`). El cambio de directorio se debe a que es recomendado no tener el fichero con las variables de entorno en el mismo directorio del repo, para evitar subir a git variables privadas.
4. El el fichero [vagrant-azure.sh](../vagrant-azure.sh), indicar en `ENV_VARS` la ruta al fichero anterior ([env_vars.sh](../env_vars.sh)).
5. Ejecutar el script [vagrant-azure.sh](../vagrant-azure.sh). El script carga las variables de entorno indicadas anteriormente y ejecuta el orden `vagrant up --provider=azure`. También se le puede indicar un parametro, que se le va a pasar a `vagrant` (ssh, halt, destroy etc). Este fichero debe estar al mismo nivel que `Vagrantfile`, que es donde se crea el fichero `.env` con las variables de entorno de vagrant.
6. Esperar a que se cree la máquina virtual y se despliegue la aplicación.
7. Enjoy.

Actualmente hay un [despliegue](http://gestfg.cloudapp.net/) en azure usando esta configuración. El despliegue estará disponible por un tiempo limitado.




