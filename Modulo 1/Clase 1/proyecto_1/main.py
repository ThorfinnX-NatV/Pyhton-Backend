from fastapi import FastAPI

#Crear una instancia de FAstAPI
app = FastAPI()

#Comienzo de la Creacion de las API - Estructura Basica
#1- Ubicar la anotacion de la instancia de FASTAPI
    #app es la clase hija que hereda todos los comportamientos de FASTAPI
@app.get("/")          #Endpoint - (Es la raiz / ) - Direccion http://127.0.0.1:8000
def inicio():          #Definicion de la funcion
    return {"Mensaje": "Dios te Bendiga Grandemente."}

