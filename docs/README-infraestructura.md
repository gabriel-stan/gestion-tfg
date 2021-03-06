
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


