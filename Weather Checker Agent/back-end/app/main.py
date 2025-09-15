from fastapi import FastAPI
from . import routes

app = FastAPI()

app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "FastAPI backend is running 🚀"}
