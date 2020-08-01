###########################
#to convert it to a PDF file
#pip install fpdf
###########################


txt_file = open('StockReport.txt', 'w')

def open_file(symbols, name):
    txt_file.write(f"------------{name} Stock Report - Created by Michael Calmette------------")

def close_file():
    txt_file.close()