from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from workflow import run_workflow
import os

app = FastAPI()

# Serve static folder at /static instead of /
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_home():
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/ask")
async def ask_ai(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "")
        result = await run_workflow(question)
        return {"answer": result["answer"]}
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
