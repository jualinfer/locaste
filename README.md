[![Build Status](https://travis-ci.org/EGC-Decide/locaste.svg?branch=master)](https://travis-ci.org/EGC-Decide/locaste)

Plataforma voto electrónico educativa
=====================================

El objetivo de este proyecto es implementar una plataforma de voto
electrónico seguro, que cumpla una serie de garantías básicas, como la
anonimicidad y el secreto del voto.

Se trata de un proyecto educativo, pensado para el estudio de sistemas de
votación, por lo que prima la simplicidad por encima de la eficiencia
cuando sea posible. Por lo tanto se asumen algunas carencias para permitir
que sea entendible y extensible.


Subsistemas, apps y proyecto base
---------------------------------

El proyecto se divide en [subsistemas](doc/subsistemas.md), los cuales estarán desacoplados
entre ellos. Para conseguir esto, los subsistemas se conectarán entre si mediante API y necesitamos un proyecto base donde configurar las ruts de estas API.

Este proyecto Django estará dividido en apps (subsistemas y proyecto base), donde cualquier app podrá ser reemplazada individualmente.

La documentación relativa a cada uno de los subsistemas puede encontrarse en la wiki:
[Subsistemas Wiki](https://github.com/EGC-Decide/locaste/wiki)


Configurar y ejecutar el proyecto
---------------------------------

Para configurar el proyecto, podremos crearnos un fichero local_settings.py basado en el
local_settings.example.py, donde podremos configurar la ruta de nuestras apps o escoger que módulos
ejecutar.

Una vez hecho esto, será necesario instalar las dependencias del proyecto, las cuales están en el
fichero requirements.txt:

    pip install -r requirements.txt

Tras esto tendremos que crearnos nuestra base de datos con postgres:

    sudo su - postgres
    psql -c "create user decide with password 'decide'"
    psql -c "create database decide owner decide"

Entramos en la carpeta del proyecto (cd decide) y realizamos la primera migración para preparar la
base de datos que utilizaremos:

    ./manage.py migrate

Por último, ya podremos ejecutar el módulos o módulos seleccionados en la configuración de la
siguiente manera:

    ./manage.py runserver

Antes de empezar a desarrollar para el proyecto, debes leer toda la documentación relativa al desarrollo del proyecto que existe en la Wiki del repositorio.
[Commits](https://github.com/EGC-Decide/locaste/wiki/Acerca-de-los-commits)
[Control de versiones](https://github.com/EGC-Decide/locaste/wiki/Control-de-versiones)
[Despliegue continuo](https://github.com/EGC-Decide/locaste/wiki/Despliegue-continuo)
[Gestión de las incidencias](https://github.com/EGC-Decide/locaste/wiki/Gesti%C3%B3n-de-las-incidencias)
[Integración continua](https://github.com/EGC-Decide/locaste/wiki/Integraci%C3%B3n-Continua)

Ejecutar con docker
-------------------
Existen varias configuraciones de docker, una para cada entorno, estas configuraciones pueden encontrarse dentro de la carpeta /docker y en su correspondiente subcarpeta.

Para el entorno de preproduccion o produccion, existen una configuracion de docker-compose que lanza 3 contenedores, uno
para el servidor de base de datos, otro para el django y otro con un
servidor web nginx para servir los ficheros estáticos y hacer de proxy al
servidor django:

 * decide\_db
 * decide\_web
 * decide\_nginx

En el caso del entorno de producción, el sistema se desplegará por defecto en el puerto 80.

En el caso del entorno de preproducción, el sistema se desplegará en el puerto 9000. (Tanto el servidor interno, como nginx)

Además se crean dos volúmenes, uno para los ficheros estáticos y medias del
proyecto y otro para la base de datos postgresql, de esta forma los
contenedores se pueden destruir sin miedo a perder datos:

 * decide\_db
 * decide\_static

Se puede editar el fichero docker-settings.py para modificar el settings
del proyecto django antes de crear las imágenes del contenedor.

Para lanzar los contenedores:

    $ cd docker
    $ docker-compose up -d

(Si quiere obtenerse la salida de los contenedores para tareas de debug, no se le especificará el parametro -d; pero este dejara los contenedores asociados a la ventana de ejecución y se cerrarán una vez finalizada la ventana)

Parar contenedores:

    $ docker-compose down

Crear un usuario administrador:

    $ docker exec -ti decide_web ./manage.py createsuperuser

Lanzar la consola django:

    $ docker exec -ti decide_web ./manage.py shell

Lanzar tests:

    $ docker exec -ti decide_web ./manage.py test

Lanzar una consola SQL:

    $ docker exec -ti decide_db ash -c "su - postgres -c 'psql postgres'"


Para el entorno de desarrollo existe un compose que despliega el entorno necesario para el proyecto a excepcion de los modulos del sistema (código).

Para ejecutarlo debe lanzarse el docker-compose que existe dentro de la carpeta docker/development.

Toda la información relativa al desarrollo y despliegue con docker, puede encontrarse en la Wiki del proyecto. 

[Docker Wiki](https://github.com/EGC-Decide/locaste/wiki/Docker)