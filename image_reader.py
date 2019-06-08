from PIL import Image
import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
import re

#pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
month_findr = re.compile(r"(January | February | March | April | May | June | July | August | September | October | November | December)")
policyNo_findr = re.compile(r"Policy No\. ([0-9/-]*)")
name_findr = re.compile(r"Policyowner(.)*\nDEAN E HARDER ([A-Z _]*)")


string = ""

pdf_path = "whole_life.pdf"
pages = convert_from_path(pdf_path)
for page in pages:
    page.save('out.jgp', 'JPEG')
    jpgOpen = Image.open('out.jgp')
    output_text = image_to_string(jpgOpen, lang='eng')
    string += output_text
print(string)
# for match in month_findr.finditer(string):
#     ans = (match.group(1))
#     print(ans)

