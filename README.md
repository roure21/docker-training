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

## Pasos

### Paso 1

Creamos el Dockerfile:

```Docker
FROM python:3.6

RUN pip install Django==3.0

COPY . /code
```

En primer lugar indicamos que queremos usar la imagen de [python](https://hub.docker.com/layers/python/library/python/3.6/images/sha256-1a5455c32fa8db385e7266850ca9604c0d8ce3416448e35b3e1e8fb24676d47b), concretamente la versión 3.6. En segundo lugar instalamos la versión de Django que necesitamos, en este caso, la versión 3.0. Finalmente, copiamos el contenido del proyecto dentro del directorio /code de la imagen.

Ahora que tenemos hecha la definición lo que nos falta es generar la imagen:

1. Nos situamos en el directorio de la aplicación: `cd elmanipulador`

2. Construimos la imagen y le damos un nombre dentro del namespace de nuestro usuario: `docker build -t <namespace>/elmanipulador .`

Una vez generada la imagen ya podemos arrancar un contenedor nuevo:
`docker run --rm -d <namespace>/elmanipulador python /code/manage.py runserver 0.0.0.0:8000`

Para verificar que la aplicación ha arrancado correctamente podemos entrar en el contenedor y hacer una petición a la aplicación:

1. Consultamos cual es el id del contenedor creado: `docker ps`

2. Abrimos una shell del contenedor: `docker exec -it <container_id> bash`

3. Hacemos una petición a la aplicación: `curl localhost:8000`

Si la respuesta es una página HTML con información de artículos quiere decir que funciona bien.

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
FROM python:3.6

RUN pip install Django==3.0

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

### Paso 7

Ahora mismo tenemos un problema a la hora de desarrollar sobre la aplicación. Cada vez que modificamos algo tenemos que volver a generar la imagen y redesplegar el contenedor para probar los cambios. Para solucionarlo podemos usar los volúmenes. Si definimos todo el código de la aplicación como volumen en el fichero `docker-compose.yml` al editarlo se actualizará automáticamente:

```yml
volumes:
  - ".:/code"
```

Hay que tener en cuenta que esto solo tiene sentido para desarrollo, en producción nunca se debería definir un volumen como este.

### Paso 8

Ahora lo que queremos hacer es dejar de tener un fichero como base de datos y empezar a usar PostgreSQL. Por ese motivo hemos creado un backup con los datos de la base de datos.

A nivel de aplicación hemos tenido que modificar el fichero `settings.py` para indicar que ahora usaremos PostgreSQL como base de datos. Esta configuración usa unos valores que se definen a nivel de variable de entorno, es decir, en el fichero `.env`. Además, tenemos que instalar el driver de PostgreSQL. Para ello hemos creado el fichero `requirements.txt` con las dependencias de la aplicación, es decir, Django y el driver de PostgreSQL. Con este cambio también hemos tenido que modficar el Dockerfile para que instale las dependencias definidas en este fichero:

```Dockerfile
FROM python:3.6

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code
```

Por otra parte, tenemos que hacer los cambios a nivel de Docker. Para ello hemos definido el servicio de PostgreSQL en el fichero `docker-compose.yml`. Básicamente definimos que queremos usar la imagen de PostgreSQL, indicamos el usuario, contraseña y nombre de la base de datos y finalmente se define un volumen para persistir los datos.

```yaml
postgres:
  image: library/postgres:10.4
  environment:
    - POSTGRES_USER=admin
    - POSTGRES_PASSWORD=secret
    - POSTGRES_DB=elmanipulador
  volumes:
    - "/opt/elmanipulador/postgresql:/var/lib/postgresql/data"
```

Además, hay que indicar al servicio de la aplicación que ahora depende del contenedor de PostgreSQL para iniciarse:

```yaml
depends_on:
  - postgres
```

Una vez aplicados estos cambios y con los contenedores anteriores eliminados, podemos levantar la aplicación con la nueva arquitectura:

1. Regeneramos la imagen de Docker ya que hemos cambiado el Dockerfile: `docker-compose build elmanipulador`

2. Levantamos todo el ecosistema: `docker-compose up -d`

3. Abrimos una shell de la aplicación: `docker-compose exec elmanipulador bash`

4. Ejecutamos las migraciones: `python manage.py migrate`

5. Salimos de la shell.

6. Importamos los datos del backup: `docker container exec -i $(docker-compose ps -q postgres) psql -Uadmin elmanipulador < backup.sql`

Y ahora ya deberíamos poder acceder a la web con la base de datos en PostgreSQL.

### Paso 9

En el último paso hemos abierto una shell para ejecutar la migraciones. En realidad, no es necesario abrir una shell para ejecutar un comando dentro, lo podemos hacer directamente: `docker-compose exec elmanipulador python manage.py migrate`. Esto también nos sirve con cualquier otro comando. Por ejemplo: `docker-compose exec elmanipulador python manage.py makemigrations`.

Por otra parte, también se pueden ejecutar los mismos comandos directamente con docker:

* `docker exec -it <container_id> python manage.py migrate`

* `docker exec -it <container_id> python manage.py makemigrations`

Otro aspecto interesante es que podemos definir un entrypoint para la imagen. De esta forma, cuando levantamos el contenedor tan solo hay que indicar los parámetros. Los pasos para hacerlo son los siguientes:

1. Modificamos el Dockerfile añadiendo al final el entrypoint: `ENTRYPOINT ["python", "manage.py"]`

2. Regeneramos la imagen: `docker-compose build elmanipulador`

3. Actualizamos el comando de la imagen de la aplicación en el docker-compose: `command: runserver 0.0.0.0:8000`

Por otra parte, si ahora queremos levantar un contenedor sin ejecutar `python manage.py` debemos indicar que queremos sobreescribir el entrypoint. Por ejemplo: `docker run --rm -it --entrypoint bash <namespace>/elmanipulador`.

### Paso 10

Una de las cosas más importantes que debemos saber es como mirar los logs. Con docker-compose es muy sencillo. Por ejemplo, para mirar los logs de la aplicación: `docker-compose logs elmanipulador`. También podemos consultar los logs directamente con docker: `docker logs <container_id>`.

Para terminar, vamos a tener que subir la imagen a DockerHub. Para subir la imagen tan solo tenemos que ejecutar el siguiente comando: `docker push <namespace>/elmanipulador`. Sin embargo, nos interesa tener versionadas las imágenes, ya que por defecto se usa el tag `latest`. Para versionar una imagen hay que ejecutar el siguiente comando: `docker tag <namespace>/elmanipulador <namespace>/elmanipulador:1.0`. Una vez hemos versionado la imagen la podemos subir al repositorio: `docker push <namespace>/elmanipulador:1.0`.

Una vez subida la imagen al repositorio de DockerHub ya está disponible para que cualquiera pueda descargarla y usarla mediante el siguiente comando: `docker pull <namespace>/elmanipulador:1.0`.
