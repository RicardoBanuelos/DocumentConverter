import os
from fastapi import HTTPException

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