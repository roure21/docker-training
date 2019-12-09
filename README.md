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
