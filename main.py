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

@app.get("/tracks/")
async def read_data(page: int = 0, per_page: int = 10):
    cursor = app.db_connection.cursor()
    page_number = page * per_page
    data = cursor.execute(
        "SELECT * FROM tracks WHERE ((trackid >= ?) AND (trackid < ?)) ORDER BY trackid ASC",
        (page_number, page_number + per_page)).fetchmany(per_page)
    return data
        

