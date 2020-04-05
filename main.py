from fastapi import FastAPI

app = FastAPI()
app.counter = 0

class request(BaseModel):
    name: str
    surename: str
    
class patient(BaseModel):
    id: int
    rec: request

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/counter')
def counter():
    app.counter += 1
    return str(app.counter)

@app.post("/patient", response_model=patient)
async def patients(rq: request):
    app.counter += 1
    return patient(id = app.counter, rec = rq)
