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

### Paso 2

Hemos visto que dentro del contenedor podemos acceder a la aplicación web. Sin embargo, no podemos acceder desde fuera. Si accedemos con el navegador a <http://localhost:8000/> veremos que nos dice 'This site can’t be reached'.

El motivo de que no funcione es que no estamos exponiendo el puerto del contenedor, y por lo tanto, nuestra máquina no tiene visibilidad de la aplicación. Para que funcione tenemos que levantar el contenedor de nuevo indicando que queremos que el puerto 8000 del contenedor sea algún puerto de nuestra máquina. En nuestro caso vamos a hacer que el puerto 8000 del contenedor se corresponda con el 9000 de nuestra máquina:

1. Consultamos el id del contenedor: `docker ps`

2. Paramos y eliminamos el contenedor: `docker rm -f <container_id>`

3. Arrancamos el contenedor enlazando los puertos: `docker run --rm -d -p 9000:8000 <namespace>/elmanipulador python /code/manage.py runserver 0.0.0.0:8000`

Ahora ya podemos acceder a <http://localhost:9000/>:

![Web Home](./images/step2.png)

### Paso 3

Queremos definir el directorio de trabajo para el contenedor. De esta forma, cualquier acción que realicemos sobre este se hará por defecto en ese directorio. Para definir el directorio de trabajo tan solo hay que añadir una línea al Dockerfile:

```Docker
FROM python:3.9

RUN pip install Django==3.1.14

COPY . /code

WORKDIR /code
```

Una vez hecho el cambio, como en cualquier otro cambio que afecte al Dockerfile, tenemos que volver a construir la imagen: `docker build -t <namespace>/elmanipulador .`

Ahora que hemos definido `/code` como el directorio de trabajo podemos redesplegar el contenedor simplificando el comando:

1. Consultamos el id del contenedor: `docker ps`

2. Paramos y eliminamos el contenedor: `docker rm -f <container_id>`

3. Arrancamos el contenedor: `docker run --rm -d -p 9000:8000 <namespace>/elmanipulador python manage.py runserver 0.0.0.0:8000`

### Paso 4

Si revisamos el fichero `settings.py` podemos ver que hay algunos valores que deberían definirse como variables de entorno. Por ese motivo modificamos el `settings.py` y definimos un nuevo fichero llamado `.env` con el siguiente contenido:

```txt
DEBUG=True
SECRET_KEY=t50lng3a!r((d^*g4l3*27!t8dd667pz!jc7me6&x!rx*3z5t1
```

Ahora debemos hacer los mismos pasos de siempre, es decir, volver a crear la imagen, borrar el contenedor y finalmente recrearlo indicándole dónde están las variables de entorno: `docker run --rm -d -p 9000:8000 --env-file .env <namespace>/elmanipulador python manage.py runserver 0.0.0.0:8000`

### Paso 5

Ahora vamos a modificar un artículo en <http://localhost:9000/admin>. Por ejemplo, vamos a poner a Paco Trampa como autor del artículo de las aves. A continuación, siguiendo el mismo procedimiento que antes, vamos a borrar y a recrear el contenedor. Sin embargo, si revisamos de nuevo el artículo, veremos que el autor vuelve a ser Fernando Mentira.

![GIF](./images/step5.gif)

Recordemos que en este caso la base de datos está en el fichero `db.sqlite3`, que forma parte de la imagen. Por lo tanto, cada vez que creamos un contenedor nuevo la base de datos se crea con la versión que contiene la imagen. Es decir, cada vez que reiniciamos un contenedor perdemos los cambios.

Para solucionarlo hay que hacer que el fichero de la base de datos persista más allá de si matamos el contenedor o no. Para eso podemos usar los volúmenes de Docker. De esta forma podremos indicar que una ruta del contenedor se corresponde con una ruta real de la máquina, y de este modo, todos los cambios que se hagan en esa ruta dentro del contenedor persistirán en la máquina.

En nuestro caso tenemos que indicar que el fichero `db.sqlite3` se monte como volumen: `docker run --rm -d -p 9000:8000 --env-file .env -v $(pwd)/db.sqlite3:/code/db.sqlite3 <namespace>/elmanipulador python manage.py runserver 0.0.0.0:8000`. Por otra parte, podemos crear el fichero `.dockerignore` con una entrada para `db.sqlite3` para indicar que no queremos que la imagen de Docker contenga este fichero, ya que siempre lo montaremos como volumen.

Ahora ya sí podemos realizar cambios sobre la base de datos y que persistan después de eliminar el contenedor.

### Paso 6

Empezamos a tener que ejecutar un comando un poco infernal para poder levantar el contenedor: `docker run --rm -d -p 9000:8000 --env-file .env -v $(pwd)/db.sqlite3:/code/db.sqlite3 <namespace>/elmanipulador python manage.py runserver 0.0.0.0:8000`. Para facilitarnos la vida podemos empezar a usar docker-compose. La misma información que contiene el comando infernal la podemos definir en el fichero `docker-compose.yml`:

```yaml
version: "3"

services:
  elmanipulador:
    image: <namespace>/elmanipulador
    build: .
    env_file: .env
    volumes:
      - "./db.sqlite3:/code/db.sqlite3"
    ports:
      - "9000:8000"
    command: python manage.py runserver 0.0.0.0:8000
```

Ahora podemos crear la imagen mediante docker-compose: `docker-compose build elmanipulador`. También podemos crear un nuevo contenedor: `docker-compose up -d elmanipulador`. Y además, ahora es mucho más fácil eliminar el contenedor: `docker-compose down`.
