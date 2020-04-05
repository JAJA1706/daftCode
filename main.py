from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
app.counter = 0
lista = []

class request(BaseModel):
    name: str
    surename: str
    
class patient(BaseModel):
    id: int
    patient: request

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/patient/{pk}")#, response_model=what)
async def patients(pk: int):
    for lol in lista:
        if pk in lista:
            return(lista[lol])
    return JSONResponse(status_code=204, content={})
    
    
       
        
   # return patient(id=app.counter, patient = pt)

@app.post("/patient", response_model=patient)
async def patients(pt: request):
    app.counter += 1
    lista.append(app.counter)
    lista.append(pt)
    return patient(id=app.counter, patient = pt)
    
       
        
   # return patient(id=app.counter, patient = pt)

@app.post("/patient", response_model=patient)
async def patients(pt: request):
    app.counter += 1
    lista.append(app.counter)
    lista.append(pt)
    return patient(id=app.counter, patient = pt)

