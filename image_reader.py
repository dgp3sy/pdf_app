from PIL import Image
import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
import re
import os
from PyPDF2 import PdfFileReader, PdfFileWriter



def prepare_name(name):
    '''
    Helper function for the process_pdf function that takes in a name with possible middle initial or middle name
    and returns the name in the format: last name, first name. This will be later used to create the file path for the
    new pdf document
    :param name: string, name in the format: first name (possible middle name) last name
    :return: name: string, in the format: last name, first name
    '''
    middle_name = False
    if name.count(' ') == 2:
        middle_name = True
    if middle_name:
        l = name.rfind(' ')
        f = name.find(' ')
        first_name = name[:f]
        last_name = name[l+1:]
    else:
        n = name.find(' ')
        first_name = name[:n]
        last_name = name[n+1:]
    return last_name+ ", " + first_name



def process_pdf(filepath):
    month_findr = re.compile(r"(January | February | March | April | May | June | July | August | September | October | November | December)")
    policyNo_findr = re.compile(r"Policy No\. ([0-9/-]*)")
    # change this to the advisor name
    name_findr = re.compile(r"Policyowner(.*?)(\n*?)DEAN HARDER ([A-Z _]*)")

    save_names = []
    pages = convert_from_path(filepath)
    for page in pages:
        page.save('out.jgp', 'JPEG')
        jpg_open = Image.open('out.jgp')
        output_text = image_to_string(jpg_open, lang='eng')

        month = None
        name = None
        policy_no = None

        for match in month_findr.finditer(output_text):
            month = match.group(1)
        for match in policyNo_findr.finditer(output_text):
            policy_no = match.group(1)
            policy_no = policy_no.replace("-","")
        for match in name_findr.finditer(output_text):
            name = match.group(3)
            name = name.strip().replace("_","")
            name = prepare_name(name)
        path_name = name + " " + policy_no + " " + month + " Annual Statement.pdf"
        save_names.append(path_name)
    return save_names


def pdf_splitter(path):
    file_names = process_pdf(path)
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = file_names[page]

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))
pdf_splitter("test_file.pdf")

