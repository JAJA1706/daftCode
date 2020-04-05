from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.post("/patient", response=patient)
def patient(rq: patient):
    return patient(received=rq.dict())

