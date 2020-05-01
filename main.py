import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')
    
@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/tracks/composers/")
async def read_data( composer_name: str ):
    cursor = app.db_connection.cursor()
    #cursor.row_factory = sqlite3.Row
    data = cursor.execute(
        "SELECT name FROM tracks WHERE composer = ?",
        (composer_name,)).fetchall()
    if len(data) == 0:
        return JSONResponse(status_code = 404, content={"error": composer_name})
    else:
        return data

