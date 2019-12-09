# Docker Training

Este proyecto consiste en un tutorial paso a paso sobre cómo dockerizar una aplicación web. Cada commit representa un cambio orientado a dockerizar la aplicación. Partimos de un estado inicial con una aplicación hecha en Django que se instala sobre la máquina directamente y terminamos con una aplicación completamente dockerizada.

## Estado inicial

Para poner en marcha la aplicación tenemos que realizar los siguientes pasos:

1. Instalar python 3.9: `sudo apt-get install python3.9`

2. Instalar pip: `sudo apt-get install python3-pip`

3. Instalar Django: `python3.9 -m pip install Django==3.1.14`

4. Aplicar las migraciones pendientes: `python3.9 elmanipulador/manage.py migrate`

5. Arrancar la aplicación: `python3.9 elmanipulador/manage.py runserver 0.0.0.0:8000`

Ahora ya podemos acceder a la [web](http://localhost:8000/) y al [backoffice](http://localhost:8000/admin/) con el usuario 'admin' y la contraseña 'admin'.

## Instalación de Docker

Antes de empezar a dockerizar la aplicación debemos [instalar](https://docs.docker.com/install/linux/docker-ce/ubuntu/) y [configurar](https://docs.docker.com/install/linux/linux-postinstall/) Docker. Además, necesitaremos tener un usuario en [DockerHub](https://hub.docker.com/) para poder guardar la imagen creada en un repositorio. Finalmente, debemos hacer login en nuestro terminal: `docker login`.

## Pasos

### Paso 1

Creamos el Dockerfile:

```Docker
FROM python:3.9

RUN pip install Django==3.1.14

COPY . /code
```

En primer lugar, indicamos que queremos usar la imagen de [python](https://hub.docker.com/layers/library/python/3.9/images/sha256-0596c508fdfdf28fd3b98e170f7e3d4708d01df6e6d4bffa981fd6dd22dbd1a5), concretamente la versión 3.9. En segundo lugar, instalamos la versión de Django que necesitamos, en este caso, la versión 3.1.14. Finalmente, copiamos el contenido del proyecto dentro del directorio /code de la imagen.

Ahora que ya tenemos lista la definición lo que nos falta es generar la imagen:

1. Nos situamos en el directorio de la aplicación: `cd elmanipulador`

2. Construimos la imagen y le damos un nombre dentro del namespace de nuestro usuario: `docker build -t <namespace>/elmanipulador .`

Una vez generada la imagen ya podemos arrancar un contenedor nuevo:
`docker run --rm -d <namespace>/elmanipulador python /code/manage.py runserver 0.0.0.0:8000`

Para verificar que la aplicación ha arrancado correctamente podemos entrar en el contenedor y hacer una petición a la aplicación:

1. Consultamos cual es el id del contenedor creado: `docker ps`

2. Abrimos una shell del contenedor: `docker exec -it <container_id> bash`

3. Hacemos una petición a la aplicación: `curl localhost:8000`

Si la respuesta es una página HTML con los artículos quiere decir que funciona bien.
