import os
from fastapi import FastAPI
from pymongo import MongoClient  # , IndexModel
from routes import router

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'Proyecto')

app = FastAPI()
app.include_router(router, tags=["travel"], prefix="/travel")


@app.on_event("startup")
def startup_db_client():
    # Conectamos a la base de datos
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]

    # Creamos índices, serán en la de airports sobre el país 'country'
    airports_collection = app.database["airports"]
    airports_collection.create_index([("country", 1)])

    # Crea índices en los campos "from", "to", y "month"
    travel_collection = app.database["travels"]
    travel_collection.create_index([("from_airport", 1)])
    travel_collection.create_index([("to_airport", 1)])
    travel_collection.create_index([("month", 1)])

    # Mostramos que se hizo la conexión
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")
