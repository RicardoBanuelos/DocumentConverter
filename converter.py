import subprocess

UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"

def docx_to_pdf(docx_path: str, pdf_path: str):
    subprocess.run(["pandoc", docx_path, "-o", pdf_path, "--pdf-engine=lualatex",
    "-V", "geometry:margin=1in"])

def xlsx_to_csv(xlsx_path: str, csv_path: str):
    pass



    

