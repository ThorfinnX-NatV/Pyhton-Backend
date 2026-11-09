# Clase 1 Introduccion a FastAPI y Estructura profesional de proyectos
> Resumed By ThorfinnX

Entrada a las aplicaciones web, y programacion Backend.b
Las API nos Brinda una especie de interfaz grafica
Se usan programas como Swagger para documentar como estan nuestras conexiones.
Lo que mas adelante nos llevaran al desarrollo Frontend y a la conexion con la persistencia de los datos, es decir Bases de Datos.

## Definicion de API

Las API son como un tipo de contrato cuando desarrollamos nuestra aplicacion.
Es la relacion que hay entre la parte grafica, es decir la que usa el usuario, las transacciones que el realiza como, crear, registrar, eliminar, (CRUD). Cada una de esas transacciones se gestionan por medio de las API, quienes reciben esa informacion y la transmiten al Backend para que este ejecute la peticion.

### Funciones de las API
Exsiten muchas funciones dentro de las APIrest pero entre tanto estas son las basicas:
- get = Leer ---- Trae todos los elementos de una persistencia
- post = Crear Registro
- get/{id} = Leer ---- Trae solo el elmento especificado
- put = Actualizar ---- Tambien puede especificarze un elemento
- delete = Eliminar ---- Lo mismo sucede con Delete

## Caracteristicas de las aplicaciones web
La forma en como se comunican los datos dentro de una aplicacion web son mediante json, o dicionarios

```json
{
    "Nombre": "Jhon",
    "Alias": "ThorfinnX",
    "Edad": "18"
}
```

## Concepto de FastAPI
Es un gestor de API Creado por un desarrollador Colombiano llamado Sebastian Ramirez, este gestor tiene su propio gestor integrado que permite probar las APIS que se llama Swagger, es un gestor muy interactivo.

FastAPI no tiene estados, lo que quiere decir que se pueden realizar 10 peticiones (Peticiones Asincronas) y estas 10 se gestionaran cada una por separado, no hay serialismo en la ejecucion, esta el paralelismo.

Es una herramienta bastante rapida, trabaja con Pydantic Libreria que entrega Tipado fuerte (Type Hint)


# Parte Practica

## Instalacion de Dependencias y Librerias para el desarrollo 

Correspondiente al Sistema operativo, en  mi caso personal uso Arch Linux como distribucion principal, por lo cual existe un proceso previo antes de comenzar con todo.

Para empezar debemos de ubicarnos en la carpeta o direccion de nuestro proyecto

- Para iniciar debemos de crear un entorno virtual en la carpeta en la que se alojara nuestro proyecto.
    ```
    python -m venv .venv
    ```
- Seguidamente activaremos el entorno virtual.
    ```
    source .venv/bin/activate
    ```
- Verificar que la ruta de activacion sea la correcta.
    ```
    which python
    ```
    Deberia de mostrar la ruta completa al archivo .venv en tu proyecto.

- Instalacion de Paquetes.\
    Es una buena practica usar un archivo requirements.txt, pues aqui escribimos todas las dependencias o librerias que sean necesarias para nuestro proyecto, sin la necesidad de confundir o averiar nuestro sistema.

    Para ello usamos.

    ```
    python -m pip install -r requirements.txt
    ```
- Seleccionar .venv como interprete de VS Code para el proyecto es un paso crucial para que no ocurra un error de sintaxis y lectura en la importacion de las librerias que hayamos agregado

    El proceso es.

    ```
    Ctrl + shift + p
    ```

    ```
    Python: Select Interpreter
    ```

    Alli mismo aparecera la ruta, o si es el caso de que no aparezca, la ultima opcion nos permite escribirla y agregarla.

    Una forma de comprobar es en la esquina inferior dercha, pues debe de aparecer 
    ```
    .venv(Version de Python)
    ```

Con esto en cuenta podremos importar las librerias y continuar con nuestro proyecto.

## Crea tu primera API

Esta es la Sintaxis Basica para la creacion de nuestra primera API

```python
from fastapi import FastAPI

#Crear una instancia de FAstAPI
app = FastAPI()

#Comienzo de la Creacion de las API - Estructura Basica
#1- Ubicar la anotacion de la instancia de FASTAPI
    #app es la clase hija que hereda todos los comportamientos de FASTAPI
@app.get("/")          #Endpoint - (Es la raiz / ) - Direccion http://127.0.0.1:8000
def inicio():          #Definicion de la funcion
    return {"Mensaje": "Dios te Bendiga."}
```

Para ejecutar uvicorn ponemos el siguiente comando en terminal.

```
uvicorn main:app --reload
```

Comando que nos dice que la instancia de FastAPI (app) se encuentra en el archivo main.

Seguido de --reload, que es una palabra reservada que nos permite que a medida que vayamos realizando cambios en nuestras paginas, estos se van a reenderizar

## Segunda API

Realizamos el mismo proceso anterior para iniciar el proceso de activacion del entorno virtual.

Pero ahora agregaremos un archivo `__init__.py` el cual nos ayuda a marcar en python la existencia de un modulo que probablemente podamos ejecutar. 

Adenmas en las herramientas del archivo de requirements agregaremos a Pydantic, el cual es el validador de fastapi.

### Implementacion de Librerias
Usaremos la misma libreria de FastAPI, pero ahora implementaremos tres Librerias nuevas.

- Base Model -  Clase que proviene de Pydantic libreria la cual nos brinda un tipo de seguridad para nuestro codigo en Python. Es como la Madre con todo lo que trata acerca de validacion en Pydantic.

- List - Que proviene de Typing es una libreria que se caracteriza por tener su inicial en mayuscula, lo que indica que es una clase integrada, tambien indica que a pesar de ser una Lista, esta tiene un **tipado fuerte**.

- Dataclass - Es una Libreria que permite que a nuestro codigo no exista la necesidad de agregar un constructor. Lo unico que se debe de realizar es Definir el nombre de la clase, sus atributos, y el tipado. No usaremos esta Libreria, pero en Pydantic usaremos una estructura similar a la de esta libreria.