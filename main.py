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
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None

def fdict(x):
    return{
        'company': 'Company',
        'address': 'Address',
        'city': 'City',
        'state': 'State',
        'country': 'Country',
        'postalcode': 'PostalCode',
        'fax': 'Fax',
    }[x]

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
    
@app.get("/customers/read/{customer_id}")
async def read_customer( customer_id: int ):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    customer = cursor.execute(
        "SELECT * FROM customers WHERE customerid = ?", (customer_id,)).fetchall()
    return customer;
    
    
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
    for x,y in update_cust.items():
        temp = fdict(x)
        lista_key.append(temp)
        lista_value.append(y)
    
    for i in range(13):
        for x,y in cust:
            if dict_key_list[i] == fdict(x):
                for z in lista_key:
                    if z == x:
                        znaleziony = True
                if znaleziony == True:
                    lista_end.append(y)
                    znaleziony = False
                else:
                    lista_end.append( cust_select[i] )
    return lista_end
            
    cursor.execute(
        "UPDATE customers SET company = ?, address = ?,  city = ?, state = ?, country = ?, postalcode = ?, fax = ?  WHERE customerid = ?", ( lista_end[0], lista_end[1], lista_end[2], lista_end[3], lista_end[4], lista_end[5], lista_end[6], customer_id,)
    )
    app.db_connection.commit()
    customer = cursor.execute(
        "SELECT * FROM customers WHERE customerid = ?", (customer_id,)).fetchone()
    return customer
    
@app.get("/sales")
async def statistics( category: str ):
    if( category == "customers" ):
        cursor = app.db_connection.cursor()
        cursor.row_factory = sqlite3.Row
        stat = cursor.execute(
        "SELECT cus.customerid as CustomerId, email, phone, ROUND( SUM(total), 2 ) AS Sum FROM customers cus JOIN invoices inv ON(cus.customerid = inv.customerid) GROUP BY cus.customerid ORDER BY Sum DESC, cus.customerid ASC"
        ).fetchall()
        return stat
    elif( category == "genres"):
        cursor = app.db_connection.cursor()
        cursor.row_factory = sqlite3.Row
        stat = cursor.execute(
        "SELECT ge.name, SUM(Quantity) AS Sum FROM genres ge JOIN tracks tr ON(ge.genreid = tr.genreid) JOIN invoice_items ii ON(ii.trackid = tr.trackid) GROUP BY ge.genreid ORDER BY Sum DESC, ge.name"
        ).fetchall()
        return stat
    else:
        return JSONResponse(status_code = 404, content={"detail":{ "error": "Podales zle category"} })
        
