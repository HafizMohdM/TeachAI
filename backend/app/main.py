from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Sahayak AI Backend Running!"}

@app.post("/generate-story")
def generate_story():
    return {"story": "Hello story!"}
