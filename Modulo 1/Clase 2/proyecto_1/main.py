from fastapi import FastAPI
from fastapi.responses import JSONResponse      #Con esto nuestras respuestas estan articuladas con un Json
from pydantic import BaseModel        #Validacion de los tipos de datos
from typing import Dict, List       #Recordad Lis, Dict, Esta Estructura tiene tipado Fuerte

app = FastAPI()

#BD - Estructura de datos
articulos: Dict[int, dict] = {}     #Diccionario de Diccionarios

#Modelo Base - Con Pydantic desde BaseModel
class ArticulosBase(BaseModel):
    nombre: str
    descripcion: str | None = None     #Significa que este campo puede estar Vacio 
    precio: float
    impuesto: float | None = None

class CrearArticulo(ArticulosBase):
    pass

class ActualizarArticulo(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    impuesto: float | None = None

class ArticulosSalida(ArticulosBase):
    id: int

@app.get("/")
def main():
    return JSONResponse(
        status_code= 200,
        content={"Bendecidos": True, "Mensaje": "Dios te Bendiga, Esto es un Terreno API"}
    )

#Consultar Articulos
@app.get("/articulos/", response_model= List[ArticulosSalida])
def obtener_articulos():
    if not articulos:
        return JSONResponse(
            status_code= 404,
            content= {"Exito": False, "Mensaje": "No Se encontraron articulos disponibles"}
        )

    lista_articulos = [ArticulosSalida(id=articulo_id, **datos).model_dump() for articulo_id, datos in articulos.items()] #Se definen las variables que se van a mostrar por medio de un for 

    return JSONResponse(
        status_code= 200,
        content={"Exito": True, "Articulos": lista_articulos}
    )

#Consultar articulo especifico
@app.get("/articulos/{articulo_id}", response_model= ArticulosSalida)
def obtener_articulo_especificoj(articulo_id: int):
    if articulo_id not in articulos:
        return JSONResponse(
            status_code= 404,
            content= {"Exito": False, "Mensaje": "El Articulo no ha sido encontrado"}
        )    
    return JSONResponse(
        status_code= 200,
        content = {"Exito": True, "Articulo": ArticulosSalida(id=articulo_id, **articulos[articulo_id]).model_dump()}
    )

@app.post("/articulos", response_model= ArticulosSalida)
def crear_articulos(articulo: CrearArticulo):
    articulo_id = len(articulos) + 1
    articulos[articulo_id] = articulo.model_dump()

    return JSONResponse(
        status_code= 201,
        content = {"Exito": True, "Mensaje": "Articulo Creado con exito", "Articulo": ArticulosSalida(id=articulo_id, **articulos[articulo_id]).model_dump()}
    )

@app.put("/articulos/{articulo_id}", response_model= ArticulosSalida)
def actualizar_articulo(articulo_id: int, articulo: ActualizarArticulo):
    if articulo_id not in articulos:
        return JSONResponse(
            status_code= 404,
            content= {"Exito": False, "Mensaje": "El Articulo no ha sido encontrado"}
        )

    articulo_guardado = articulos[articulo_id]
    datos_actualizados = articulo.model_dump(exclude_unset= True)   #unset significa que no se guarde en el Json, los atributos que no cambiaron, solo guarda los modificados, y no sobrecarga red
    articulo_guardado.update(datos_actualizados)
    articulos[articulo_id] = articulo_guardado

    return JSONResponse(
        status_code= 200,
        content = {"Exito": True, "Mensaje": "Articulo actualizado Exitosamente", "Articulo": ArticulosSalida(id= articulo_id, **articulo_guardado).model_dump()}
    )

@app.delete("/articulos/{articulo_id}", response_model= ArticulosSalida)
def eliminar_articulo(articulo_id: int):
    if articulo_id not in articulos:
            return JSONResponse(
                status_code= 404,
                content= {"Exito": False, "Mensaje": "El Articulo no ha sido encontrado"}
            )

    articulo_eliminado = articulos.pop(articulo_id)      #Con Pop Se muestra el articulo hasta despues de ser eliminado.
    
    return JSONResponse(
        status_code= 200,
        content = {"Exito": "True", "Mensaje": f"Articulo {articulo_id} eliminado exitosamente", "Articulo": ArticulosSalida(id= articulo_id, **articulo_eliminado).model_dump()}
    )

