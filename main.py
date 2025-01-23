import os
import shutil
from uuid import uuid4

import uvicorn
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

supported_conversion_dict = {
    ".docx": {".pdf"},
    ".xlsx": {".csv"}
}

def get_file_extension(filename: str):
    split_tup = os.path.splitext(filename)
    return split_tup[1]

def validate_file(filename: str) -> bool:
    if get_file_extension(filename) not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

def validate_file_exists(file_path) -> bool: 
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

def validate_conversion(initial_format: str, target_format: str):
    if initial_format not in supported_conversion_dict:
        raise HTTPException(status_code=500, detail="Invalid file found")
    
    if target_format not in supported_conversion_dict[initial_format]:
        raise HTTPException(status_code=400, detail="Unsupported conversion type")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    validate_file(file.filename)
    
    file_id = str(uuid4())
    file_extension = get_file_extension(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}{file_extension}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename" : f"{file_id}{file_extension}"
    }

@app.get("/convert_docx_to_pdf")
async def convert_docx_to_pdf(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    validate_file_exists(file_path)
    
    TARGET_FORMAT = ".pdf"

    file_extension = get_file_extension(filename)
    validate_conversion(file_extension, TARGET_FORMAT)

    output_filename =  f"{str(uuid4())}{TARGET_FORMAT}"
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    docx_to_pdf(file_path, output_path)

    return {
        "filename" : output_filename
    }

@app.get("/convert_xlsx_to_csv")
async def convert_xlsx_to_csv(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    validate_file_exists(file_path)

    TARGET_FORMAT = ".csv"

    file_extension = get_file_extension(filename)
    validate_conversion(file_extension, TARGET_FORMAT)

    output_folder = str(uuid4())
    output_path = os.path.join(CONVERTED_FOLDER, output_folder)

    os.makedirs(output_path, exist_ok=True)

    xlsx_to_csv(file_path, output_path)

    return {
        "folder_name": output_folder
    }

@app.get("/download/file")
async def download_file(filename: str):
    file_path = os.path.join(CONVERTED_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

@app.get("/download/folder")
async def download_file(folder_name: str):
    folder_path = os.path.join(CONVERTED_FOLDER, folder_name)

    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Folder not found")
    
    output_path = os.path.join(CONVERTED_FOLDER, folder_name)
    zip_path = shutil.make_archive(output_path, "zip", folder_path)
    
    return FileResponse(zip_path, media_type="application/octet-stream", filename=f"{folder_name}.zip")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
