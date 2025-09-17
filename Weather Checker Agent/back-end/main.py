# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS setup (React se request allow karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev mode me * chalega, prod me specific domain do
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Simple test route
@app.get("/")
def hello():
    return {"message": "Hello from FastAPI!"}