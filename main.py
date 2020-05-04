import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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

class Customer(BaseModel):
    Company: str = None
    Address: str = None
    City: str = None
    State: str = None
    Country: str = None
    PostalCode: str = None
    Fax: str = None

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
    return JSONResponse(status_code = 200, content={"AlbumId": album_id, "Title": album[0][1], "ArtistId": album[0][2]})
    
    
@app.put("/customers/{customer_id}")
async def update_cust(customer_id: int, cust: Customer):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    cust_select = cursor.execute(
        "SELECT * FROM customers WHERE customerid = ?", (customer_id,)).fetchone()
    if cust_select is None:
        return JSONResponse(status_code = 404, content={"detail":{ "error": "Podales zle id customer"} })
        
    lista_key = []
    lista_value = []
    lista_end = []
    znaleziony = False
    dict_key_list = cust_select.keys()
    update_cust = cust.dict(exclude_unset=True)
    temp = "huk"
    for x,y in update_cust.items():
        lista_key.append(x)
        lista_value.append(y)
        
    for i in range(13):
        for x,y in cust:
            if dict_key_list[i] == x:
                for z in lista_key:
                    if z == x:
                        znaleziony = True
                if znaleziony == True:
                    lista_end.append(y)
                    znaleziony = False
                else:
                    lista_end.append( cust_select[i] )
            
    cursor.execute(
        "UPDATE customers SET company = ?, address = ?,  city = ?, state = ?, country = ?, postalcode = ?, fax = ?  WHERE customerid = ?", ( lista_end[0], lista_end[1], lista_end[2], lista_end[3], lista_end[4], lista_end[5], lista_end[6], customer_id,)
    )
    app.db_connection.commit()
    customer = cursor.execute(
        "SELECT * FROM customers WHERE customerid = ?", (customer_id,)).fetchall()
    return JSONResponse(status_code = 200, content={
        "CustomerId": customer[0][0],
        "FirstName": customer[0][1],
        "LastName": customer[0][2],
        "Company": customer[0][3],
        "Address": customer[0][4],
        "City": customer[0][5],
        "State": customer[0][6],
        "Country": customer[0][7],
        "PostalCode": customer[0][8],
        "Phone": customer[0][9],
        "Fax": customer[0][10],
        "Email": customer[0][11],
        "SupportRepId": customer[0][12]})