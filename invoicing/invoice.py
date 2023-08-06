import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, image, product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    This function reads Excel invoices and generates PDF invoices
    :param invoices_path:
    :param pdfs_path:
    :param image:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    # Read all the files in /invoices/
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")
    
    # For each file, create a PDF Invoice
    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="Letter")
        pdf.add_page()
        
        # Generate Invoice # and Date at the top of each page
        filename = Path(filepath).stem
        invoice_no, date = filename.split("-")
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice #: {invoice_no}", ln=1)
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
        pdf.cell(w=50, h=8, txt=" ", ln=1)
      
        df = pd.read_excel(filepath, sheet_name="Sheet 1")
    
        # Start creating table
        # Add a header
        columns = [item.replace("_", " ").title() for item in df.columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=32, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)
    
        # Add rows to table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=32, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)
        
        # Add a total row to table
        total = df[total_price].sum()
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, 59, 202, 59)
        pdf.cell(w=30, h=8, txt=" ", border=1)
        pdf.cell(w=70, h=8, txt=" ", border=1)
        pdf.cell(w=32, h=8, txt=" ", border=1)
        pdf.cell(w=30, h=8, txt=" ", border=1)
        pdf.cell(w=30, h=8, txt=str(total), border=1, ln=1)
        
        # Add total due
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=8, txt=" ", ln=1)
        pdf.cell(w=30, h=8, txt=f"The total amount due is ${total}", ln=1)
        
        # Add company name and logo
        pdf.cell(w=25, h=8, txt=f"PythonHow")
        pdf.image(image, w=10)
        
        if not os.path.isdir(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
    