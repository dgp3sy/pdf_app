import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import regular_expressions
from doc_num import doc_enum
from doc_num import doc_to_string
import time
import os
def search_document(regex_buildr, text):
    month = regex_buildr.find_month(text) + " "
    year = regex_buildr.find_year(text) + " "
    policy_no = regex_buildr.find_policyNo(text) + " "
    name = regex_buildr.find_name(text) + " "

    return month, year, policy_no, name
def file_name_generator(filepath, file_type):
    '''
    Generates file path names in the format: Last Name, First Name Policy_Number Month Annual Report.pdf
    First, this function reads the pdf, converts to jpeg format, uses optimal character recognition (OCR)
    to determine the text of the pdf document. This text is then searched using regular expressions for the
    necessary values including name, policy number and month. The file name is comprised accordingly
    :param filepath: path of the original pdf document - containing multiple annual reports
    :param file_type: integer value mapping to the type of file you are attempting to process
        1 : Old Annual Report Format
        2 : New Annual Report Format
        3 : Term Life Annual Report
        4 : IDO Letter
    :return: list of the valid save names of all reports in that document
    '''
    if file_type == doc_enum.OLD.value:
        doc_len = 1
    else:
        doc_len = 2
    save_names = []
    # Split entire pdf document into its own page and analyze text

    pages = convert_from_path(filepath)
    output_text = ""
    count = 0
    output_text_list = []
    # put the text of pages into list - grouping by pairs of two pages
    for page in pages:
        count += 1
        # save a jpeg to allow for easier OCR (optimal character recognition)
        page.save('out.jgp', 'JPEG')
        jpg_open = Image.open('out.jgp')
        output_text += image_to_string(jpg_open, lang='eng')  # output OCR to string

        # Generate New Document Name
        if count == doc_len:
            print("Processing Page", page, "...")
            output_text_list.append(output_text)
            output_text = ""
            count = 0


    # Pick Regular Expression
    if file_type == doc_enum.OLD.value:
        # set the month based on the New Annual Report Regex
        reg_builder = regular_expressions.old_annual_regex()
    elif file_type == doc_enum.NEW.value:
        reg_builder = regular_expressions.new_annual_regex()
    elif file_type == doc_enum.TERM.value:
        reg_builder = regular_expressions.term_regex()
    else:
        reg_builder = regular_expressions.ido_regex()

    # extract information from each policy owner's form
    for text in output_text_list:
        # CREATE FILE NAME
        month, year, policy_no, name = search_document(reg_builder, text)
        path_name = name + policy_no + month + year + doc_to_string(file_type)
        save_names.append(path_name)  # append to path name
    return save_names


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


def init(path, doc_type, is_test=False):
    '''
        Initializes the pdf processor: takes in the path of the original file, calls the new_file_name_generator() helper
        method in order to determine new file names. Splits the pdf document by each page and saves them
        :param path: the file path of the original document
        :return: none, generates n new files where n is the length of the pdf document
        '''
    if doc_type == doc_enum.OLD.value:
        # creates file names as per user's original requirements
        file_names = file_name_generator(path, doc_type)
        pages = 1
    elif doc_type == doc_enum.NEW.value:
        file_names = file_name_generator(path, doc_type)
        pages = 2
    else:
        file_names = file_name_generator(path, doc_type)
        pages = 2

    # Generates Save Location for Files
    save_location = generate_save_location(is_test)

    # splits by page and saves the files to location
    pdf = PdfFileReader(path, strict=False)
    for page in range(0, pdf.getNumPages(), pages):
        if (page != "NONE"):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))

            # select appropriate file name based on the generator
            output_filename = file_names[page//pages]

            # saves the file to the appropriate destination
            with open(save_location+output_filename, 'wb') as out:
                pdf_writer.write(out)



pytesseract.pytesseract.tesseract_cmd =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# times the process
# start_time = time.time()
# init_old("C:\\Users\\jmper\\Documents\\Scans\\2019-11-26_103051.pdf")
# init_old("test2.pdf")
# print("--- %s seconds ---" % (time.time() - start_time))

# init("D:\IDO Letter 2.pdf", 4)