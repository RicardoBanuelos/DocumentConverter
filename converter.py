from docx2pdf import convert

import pandas as pd

UPLOAD_FOLDER = "uploads/"
CONVERTED_FOLDER = "converted/"

def docx_to_pdf(docx_path: str, pdf_path: str):
    convert(docx_path, pdf_path)

def xlsx_to_csv(xlsx_path: str, output_path: str):
    df = pd.read_excel(xlsx_path, sheet_name=None)

    for sheet, data in df.items():
        csv_path = f"{output_path}/{sheet}.csv"
        data.to_csv(csv_path, index=False)





    

