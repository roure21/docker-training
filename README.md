# Docker Training

Este proyecto consiste en un tutorial paso a paso de como dockerizar una aplicación web. Cada commit consiste en un cambio orientado a dockerizar la aplicación. Partimos de un estado inicial con una aplicación hecha en Django que se instala sobre la máquina directamente y terminamos con una aplicación completamente dockerizada.

## Estado inicial

Para poner en marcha la aplicación tenemos que realizar los siguientes pasos:

1. Instalar python 3.6: `sudo apt-get install python3.6`

2. Instalar pip: `sudo apt-get install python3-pip`

3. Instalar django: `python3.6 -m pip install Django==3.0`

4. Arrancar la aplicación: `python3.6 elmanipulador/manage.py runserver 0.0.0.0:8000`

Ahora ya podemos acceder a la web en <http://localhost:8000/> y al backoffice en <http://localhost:8000/admin/> con el usuario 'admin' y la contraseña 'admin'.

## Instalación de Docker

Antes de empezar a dockerizar la aplicación debemos [instalar](https://docs.docker.com/install/linux/docker-ce/ubuntu/) y [configurar](https://docs.docker.com/install/linux/linux-postinstall/) Docker. Además, necesitaremos tener un usuario en [DockerHub](https://hub.docker.com/) para poder guardar la imagen creada en un repositorio. Finalmente, debemos hacer login en nuestro terminal: `docker login`.
