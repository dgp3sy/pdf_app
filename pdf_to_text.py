from PIL import Image
import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
import re

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
