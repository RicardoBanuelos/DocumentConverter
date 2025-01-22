import os
import shutil
from uuid import uuid4

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from converter import docx_to_pdf, xlsx_to_csv

app = FastAPI()

UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"

@app.get("/")
async def  root():
    return {"message" : "Hello World"}

ALLOWED_EXTENSIONS = {'.docx', '.xlsx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

conversion_dict = {
    ".docx": {
        ".pdf": docx_to_pdf
    }
}

def get_file_extension(filename: str):
    split_tup = os.path.splitext(filename)
    return split_tup[1]

def file_is_valid(filename: str) -> bool:
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file_is_valid(file.filename):    
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_id = str(uuid4())
    file_extension = get_file_extension(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}{file_extension}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename" : f"{file_id}{file_extension}"
    }

@app.get("/convert")
async def convert_file(filename: str, target_format: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_extension = get_file_extension(filename)

    if file_extension not in conversion_dict:
        raise HTTPException(status_code=500, detail="Invalid file found")
    
    if target_format not in conversion_dict[file_extension]:
        raise HTTPException(status_code=400, detail="Unsupported conversion type")
    
    output_filename =  f"{str(uuid4())}{target_format}"
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    conversion_dict[file_extension][target_format](file_path, output_path)

    return {
        "filename" : output_filename
    }

@app.get("/download")
async def download_file(filename: str):
    file_path = os.path.join(CONVERTED_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


