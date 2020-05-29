import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import process_pdf
import time
import re
import os

def prepare_month(num):
    '''
    Converts integers to string value of month using dictionary
    :param num: (int) Integer value of month, expected values: 1-12
    :return: (str) String value that corresponds to that integer's month
    '''
    month_dict = {
        1:"January",
        2:"February",
        3:"March",
        4:"April",
        5:"May",
        6:"June",
        7:"July",
        8:"August",
        9:"September",
        10:"October",
        11:"November",
        12:"December"
    }
    return month_dict.get(num, "MONTH ")
def ido_name_generator(filepath):
    '''

    :param path:
    :return:
    '''
    date_findr = re.compile(r"Anniversary Date: ([0-9]{2})/([0-9]{2})/([0-9]{4})")
    policy_no_findr = re.compile(r"Policy Number: ([0-9]*)")
    name_findr = re.compile(r"Dear ([A-Za-z ]*),")

    pages = convert_from_path(filepath)
    output_text = ""
    count = 0
    doc_text_split = []
    # Builds list of text for grouping
    for page in pages:
        # print("Processing Page", page, "...")
        count += 1

        # save a jpeg to allow for easier OCR (optimal character recognition)
        page.save('out.jgp', 'JPEG')
        jpg_open = Image.open('out.jgp')
        output_text += image_to_string(jpg_open, lang='eng')  # output OCR to string

        if count == 4:
            doc_text_split.append(output_text)
            output_text = ""
            count = 0
    doc_names = []
    for i in range(len(doc_text_split)):
        output_text = doc_text_split[i]

        # placeholder for new file name values
        month = "MONTH "
        year = "YEAR "
        policy_no = "POLICY_NO "
        name = "NAME"

        for match in date_findr.finditer(output_text):
            month = match.group(1)
            month = prepare_month(int(month))+" "
            year = match.group(3)+" "
        # set the policy number based on regex established
        for match in policy_no_findr.finditer(output_text):
            policy_no = match.group(1)
            policy_no = policy_no.replace("-", "")+" "

        for match in name_findr.finditer(output_text):
            name = match.group(1).strip()
            name = process_pdf.prepare_name(name)

        # CREATE FILE NAME
        path_name = name + " " + policy_no + month + year + "IDO Letter.pdf"
        doc_names.append(path_name)  # append to path name
    return doc_names


def init_ido_reader(path):
    '''

    :param path: file path of the IDO Letter
    :return: None, generates new pdf files from pages
    '''

    # Creates file names based on user requirements for IDO Letters
    file_names = ido_name_generator(path)
    num_pages = 4

    # Get file path of desktop - extract to folder
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    save_location = desktop+"\\Extracted Pages\\"

    # manual override of save location here
    # save_location = "C:\\Users\\jmper\\Desktop\\Extracted Pages\\"

    pdf = PdfFileReader(path, strict=False)
    for i in range(0, pdf.getNumPages(), num_pages):
        if (i != "NONE"):
            pdf_writer = PdfFileWriter()
            for j in range(num_pages):
                pdf_writer.addPage(pdf.getPage(i + j))

            # select appropriate file name based on the generator
            output_filename = file_names[i//num_pages]

            # TODO: save to a user defined location
            # saves the file to the appropriate destination
            with open(save_location + output_filename, 'wb') as out:
                pdf_writer.write(out)

