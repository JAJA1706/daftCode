from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.counter = 0

class request(BaseModel):
    name: str
    surename: str
    
class patient(BaseModel):
    id: int
    patient: request

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.post("/patient", response_model=patient)
async def patients(pt: request):
    app.counter += 1
    return patient(id=app.counter, patient = pt)
