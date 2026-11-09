from fastapi import FastAPI, HTTPException #esta es una clase de FastApi que permite gestionar errores.
from pydantic import BaseModel  #Pydantic da un tipo de seguridad a FastAPI
from typing import List     #El List con Mayuscula a parte de ser una clase integrada

app = FastAPI()

#Se crea el modelo de Respuesta
class Cliente(BaseModel):
    id: int
    nombre: str
    edad: int

#Creacion de "Base de Datos"
clientes_db: List[Cliente] = []

#Acumulador - Cada vez que se cree un nuevo reistro se cree uno nuevo, lo que permite que guarde y genere nuevos id
contador_id = 1

#Uso de Apirest - CRUD

#Raiz
@app.get("/")
async def inicio():
    return {"Mensaje": "Bienvenidos sean, Dios les Bendiga"}

#1- Crear un cliente
@app.post("/clientes", response_model=Cliente)   #Response Model - Define y valida que estructura debe devolver un endpoint de una API
async def crear_cliente(cliente: Cliente):      #Async se usa para aplicaciones reales fuera de un servidor local
    global contador_id
    cliente.id = contador_id
    clientes_db.append(cliente)
    contador_id += 1
    return cliente

#Listar los todos los elementos de la persistencia
@app.get("/clientes", response_model=List[Cliente])
async def listar_lientes():
    return clientes_db

#Listar elemento especifico
@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def obtener_cliente(cliente_id: int):
    for cliente in clientes_db:
        if cliente.id == cliente_id:
            return cliente
        
    raise HTTPException(status_code=404, detail="El Cliente no ha sido encontrado") #raise - Nos permite personalizar un error que ocurra en nuestra app, permitiendo que no quede por defecto

#Actualizar un registro 
@app.put("/clientes/{cliente_id}", response_model= Cliente)
async def actualizar_clientes(cliente_id: int, cliente_actualizado: Cliente):
    for cliente in clientes_db:
        if cliente.id == cliente_id:
            cliente.nombre = cliente_actualizado.nombre
            cliente.edad = cliente_actualizado.edad
            return cliente
    
    raise HTTPException(status_code=404, detail="El Cliente no ha sido encontrado")

#Eliminar un Registro 
@app.delete("/clientes/{cliente_id}", response_model = Cliente)
async def eliminar_clientes(cliente_id: int):
    for cliente in clientes_db:
        if cliente.id == cliente_id:
            clientes_db.remove(cliente)
            return {"Mensaje":f"Cliente con id {cliente_id} eliminado con exito"}
    
    raise HTTPException(status_code=404, detail="El Cliente no ha sido encontrado")

