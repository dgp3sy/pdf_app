import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
from joblib import Parallel, delayed
from PIL import Image
import regular_expressions
import time
import re
import os


def ido_name_generator(filepath):
    '''
    :param filepath: location of the document
    :return: list of strings of the filenames
    '''
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

        regex_buildr = regular_expressions.ido_regex()
        name = regex_buildr.find_name(output_text)+" "
        policy_no = regex_buildr.find_policyNo(output_text)+" "
        month = regex_buildr.find_month(output_text)+" "
        year = regex_buildr.find_year(output_text)+" "

        # CREATE FILE NAME
        path_name = name + policy_no + month + year + "IDO Letter.pdf"
        doc_names.append(path_name)  # append to path name
    return doc_names

def generate_save_location(is_test):
    '''
    preconditions: User has a filepath to their Desktop which is named "Desktop" and is using the Windows Operating System
    postconditions: filepath to folder exists

    This subroutine first generates the filepath of the desktop, then generates a filepath to store folders. If the folder
    does not exist then it is created, so that the extracted pages can be stored there

    :param is_test: Boolean Value of to determine if the extracted folders should end up in the testing environment
    folder (default value is false)
    :return: str value of the filepath to which the files should be written
    '''
    # Get file path of desktop - extract to folder
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # manual override of save location here
    # save_location = "C:\\Users\\jmper\\Desktop\\Extracted Pages\\"

    # If this is a testing environment, the save location will create a testing environment folder
    if is_test:
        save_location = desktop + "\\Extracted Pages Testing Environment\\"
    else:
        save_location = desktop + "\\Extracted Pages\\"

    if not os.path.exists(save_location):
        os.makedirs(save_location)

    return save_location


def init_ido_reader(path, is_test=False):
    '''

    :param path: file path of the IDO Letter
    :return: None, generates new pdf files from pages
    '''

    # Creates file names based on user requirements for IDO Letters
    file_names = ido_name_generator(path)
    num_pages = 4

    save_location = generate_save_location(is_test)

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

