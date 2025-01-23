from docx2pdf import convert

UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"

def docx_to_pdf(docx_path: str, pdf_path: str):
    convert(docx_path, pdf_path)

def xlsx_to_csv(xlsx_path: str, csv_path: str):
    pass



    

