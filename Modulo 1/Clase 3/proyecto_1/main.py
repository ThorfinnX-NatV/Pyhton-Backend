#TEMA CENTRAL - VALIDACION DE APIS
from fastapi import FastAPI, APIRouter, HTTPException, status      #APIRouter permite personalizar la instancia de FastApPi
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field       #Con el campo Field Personalizamos las APIs
from typing import Dict, List, Optional

#Clases para Recursos
class RecursoBase(BaseModel):
    nombre: str = Field(..., min_length= 3, max_length= 50, description= "Nombre del Recurso", examples= ["Seis Piesas Faciles"])     #Establece una estructura, incluso valores por defecto de inicio.
    descripcion: Optional[str] = Field(None, max_length= 200, description= "Descripcion opcional del recurso", examples=["Resume los conceptos mas importantes de la Fisica, con un estilo claro y brillante"])      #No no es igual a un espacio en Blanco
    autor: str = Field(..., min_length= 4, max_length= 40, description= "Autor del Recurso", examples= ["Richard P. Feyman"]) 
    categoria: str = Field(..., min_length= 4, max_length= 50, description= "Categoria a la que pertenece el recurso de Estudio", examples= ["Fisica y Matematicas"] )
    
class CreateRecurso(RecursoBase):
    pass




class UpdateRecurso(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length= 50, examples= ["Recurso Actualizado"] )
    descripcion: Optional[str] = Field(None, max_length= 200, description= "Descripcion opcional del recurso", examples=["Nueva descripcion"])

class RecursoResponse(RecursoBase):
    item_id: int = Field(..., gt= 0, description= "ID Unico del Recurso")

#Clases para Usuarios
class UsusarioBase(BaseModel):
    username: str = Field(..., min_length= 4, max_length= 16, description= "Nombre de Usuario", examples= ["ThorfinnX"] )
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", description= "Correo electronico valido", examples= ["thorfinnx.23@gmail.com"])
    edad: int = Field(..., gt= 0, lt= 121, description= "Edad entre 1 y 120 años", examples=[25])

class CreateUsuario(UsusarioBase):
    pass

class UpdateUsuario(BaseModel):
    username: Optional[str] = Field(None,min_length= 4, max_length= 16, examples= ["Nuevo Usuario"])
    email: Optional[str] = Field(None, attern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", examples= ["Nuevo correo de Usuario"])
    edad: Optional[int] = Field(None, gt= 0, lt= 121, examples=["Edad Actualizada"])

class UsuarioResponse(UsusarioBase):
    user_id: int = Field (..., gt= 0, description= "ID Unico del Usuario")

#Estructura de Datos
#Recursos
db_recursos: List[Dict] = []
next_recurso_id = 1

#Usuarios
db_usuarios: List[Dict] = []
next_usuario_id = 1

#Personalizacion de las APIS
recursos_router = APIRouter(                #Se usa APIRouter para personalizar las API
    prefix= "/recursos",
    tags= ["APIRecursos"],                  #Tags = Se usa para documentar.
    responses= {404: {"Description": "Recurso no Encontrado"}}
)     

usuarios_router = APIRouter(
    prefix="/usuarios",
    tags= ["APIUsuarios"], 
    responses= {404: {"Description": "Usuario no Encontrado"}}
) 

#Creacion de las API
#Crear un Recurso
@recursos_router.post(
    "/",
    response_model= RecursoResponse,
    status_code= status.HTTP_201_CREATED,
    summary= "Crear un Recurso nuevo"
)
async def crear_recurso(recurso: CreateRecurso):
    global next_recurso_id
    new_item = recurso.model_dump()         #Model_dump se usa para convertir el modelo de datos en un Diccionario estandar de Python
    new_item["item_id"] - next_recurso_id
    db_recursos.append(new_item)
    next_recurso_id += 1
    return new_item

#Consultar todos los Recursos
@recursos_router.get(
    "/",
    response_model=List[RecursoResponse],
    summary= "Obtener todos los recursos"
)
async def get_all_recursos():
    return db_recursos

#Consultar un Recurso
@recursos_router.get(
    "/{item_id}",
    response_model= RecursoResponse, 
    summary = "Obtener un recurso"
)
async def read_recurs(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code= 422, detail= "El ID de Recurso es Invalido")        #raise personaliza el Mensaje de la Exepcion
    for item in db_recursos:
        if item["item_id"] == item_id:
            return item
        raise HTTPException(status_code= 404, detail= "El recurso no ha sido encontrado")

@recursos_router.get(
    "/{item_id}",
    response_model=  RecursoResponse,
    summary = "Actualizar un recurso existente"
)
async def update_recurso(item_id: int, recurso:UpdateRecurso):
    if item_id <= 0:
        raise HTTPException(status_code= 422, detail= "El ID de Recurso es Invalido")
    for item in db_recursos:
        if item["item_id"] == item_id:
            update_data = recurso.model_dump(exclude_unset= True)
            item.update(update_data)
            return item
        raise HTTPException(status_code= 404, detail="El Recurso no ha Sido Encontrado")

@recursos_router.delete(
    "/{item_id}",
    status_code= status.HTTP_200_OK,
    summary = "Eliminar Recurso"
)
async def delete_recurso(item_id: int):
    global db_recursos
    for item in db_recursos:
        if item["item_id"] == item_id:
            db_recursos.remove(item)
            return{"Mensaje": "Recurso Eliminado con Exito"}

#=============================================================================================
#PUNTO DE ENTRADA ---- Exclusivo para Uvicorn
#=============================================================================================

#Crearemos una Instacia de FastAPi, para Traerla y asimismo levantar el Servidor

app = FastAPI(
    title= "API de Recursos y Usuarios",    
    description= "Ejercicio de APIs con FastAPI, APIRouter persoalizados, validacion con Pydantic y base en memoria",
    version= "2.0.0" 
)

@app.get("/", summary= "Pagina de Inicio de la API")
async def root():
    return {
        "mensaje": "Bienvenido a la API de Recursos y Usuarios",
        "version": "2.0.0",
        "documentacion": "/docs",
        "endpoints": {
            "recursos": "/recursos",
            "usuarios": "/usuarios"
        }
    }

#Incluir las Rutas personalizadas
app.include_router(recursos_router)
app.include_router(usuarios_router)

#Metodo de ejecucuion Unico para Uvicorn
if __name__ ==  "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host= "127.0.0.1",
        port= 8000,
        reload= True,
        log_level= "info"
    )


#CheckList - Que se debe de realizar para culminar el proyecto
#Mejorar las API de Recursos
#Crear las API de Usuarios
#Agregar Attributos a cada Metodo en la API, 5 por cada Metodo.