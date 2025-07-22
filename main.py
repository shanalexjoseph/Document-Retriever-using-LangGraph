from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import shutil
import uuid

# ✅ Updated import from modular graph_runner
from workflow.graph_runner import run_pdf_workflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("frontend/index.html")


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process_doc")
async def process_doc(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = run_pdf_workflow(file_path)
        os.remove(file_path)
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/process_doc_multiple")
async def process_doc_multiple(files: list[UploadFile] = File(...)):
    results = []
    try:
        for file in files:
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            result = run_pdf_workflow(file_path)
            os.remove(file_path)
            results.append(result)

        return JSONResponse(content=results)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
