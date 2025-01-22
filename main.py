import os
import shutil
from uuid import uuid4

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"

@app.get("/")
async def  root():
    return {"message" : "Hello World"}

ALLOWED_EXTENSIONS = {'docx', 'xlsx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

def file_is_valid(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file_is_valid(file.filename):    
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id" : file_id,
        "filename" : file.filename
    }

@app.get("/download")
async def download_file(file_id: str):
    converted_files = os.listdir(CONVERTED_FOLDER)

    file_name = None

    for file in converted_files:
        if file.startswith(file_id):
            file_name = file
            break

    if file_name is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = os.path.join(CONVERTED_FOLDER, file_name)
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)


