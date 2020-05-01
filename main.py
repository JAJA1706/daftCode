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


@app.get("/patient/{pk}")
async def patients(pk: int):
    for lol in lista:
        if pk in lista:
            return(lista[lol+1])
    return JSONResponse(status_code=204, content={})
    
    #looool
       

@app.post("/patient", response_model=patient)
async def patients(pt: request):
    lista.append(app.counter)
    lista.append(pt)
    app.counter += 1
    return patient(id=app.counter, patient = pt)
    
       

