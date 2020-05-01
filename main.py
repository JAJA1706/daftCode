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

class Album(BaseModel):
    title: str
    artist_id: int


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/tracks/composers/")
async def read_data( composer_name: str ):
    cursor = app.db_connection.cursor()
    #cursor.row_factory = sqlite3.Row
    cursor.row_factory = lambda cursor, x: x[0]
    data = cursor.execute(
        "SELECT name FROM tracks WHERE composer = ? ORDER BY name",
        (composer_name,)).fetchall()
    if len(data) == 0:
        return JSONResponse(status_code = 404, content={"detail":{ "error": composer_name} })
    else:
        return data

@app.post("/albums")
async def post_data(album: Album):
    cursor = app.db_connection.cursor()
    cursor.row_factory = lambda cursor, x: x[0]
    artist_check = cursor.execute(
    "SELECT count(artistid) FROM artists WHERE artistid = ?",
    (album.artist_id,)).fetchall();
    if artist_check[0] == 0:
        return JSONResponse(status_code = 404, content={"detail":{ "error": "Podales zle id artysty"} })
        
    cursor.execute(f"Insert INTO albums (title, artistid) VALUES (?,?)",(album.title, album.artist_id,))
    app.db_connection.commit()
    new_id = cursor.lastrowid
    cursor.row_factory = sqlite3.Row
    #album = app.db_connection.execute(
    #    """SELECT albumid AS AlbumId, title as Title, artistid AS ArtistId FROM albums where albumid = ?""", (new_id,)).fetchone() 
    return JSONResponse(status_code = 201, content={"AlbumId": new_id, "Title": album.title, "ArtistId": album.artist_id})
    
    
@app.get("/albums/{album_id}")
async def read_album( album_id: int ):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    album = cursor.execute(
        "SELECT * FROM albums WHERE albumid = ?", (album_id,)).fetchall()
    return album
    
        
    
    