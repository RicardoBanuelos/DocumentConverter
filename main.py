import os
from fastapi import FastAPI, File, UploadFile, HTTPException

import shutil
from uuid import uuid4

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

