import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import regular_expressions
import time
import os

def file_name_generator_new(filepath):
    '''
    Generates file path names in the format: Last Name, First Name Policy_Number Month Annual Report.pdf
    First, this function reads the pdf, converts to jpeg format, uses optimal character recognition (OCR)
    to determine the text of the pdf document. This text is then searched using regular expressions for the
    necessary values including name, policy number and month. The file name is comprised accordingly
    :param filepath: path of the original pdf document - containing multiple annual reports
    :return: list of the valid save names of all reports in that document
    '''

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
        if count == 2:
            print("Processing Page", page, "...")
            output_text_list.append(output_text)
            output_text = ""
            count = 0

    # extract information from each policy owner's form
    for text in output_text_list:
        # set the month based on the regex established
        reg_builder = regular_expressions.new_annual_regex()
        month = reg_builder.find_month(text)+" "
        year = reg_builder.find_year(text)+" "
        policy_no = reg_builder.find_policyNo(text)+" "
        name = reg_builder.find_name(text)+" "

        # CREATE FILE NAME
        path_name = name + policy_no + month + year + "Annual Statement.pdf"
        save_names.append(path_name)  # append to path name
    return save_names

def file_name_generator_old(filepath):
    '''
    Generates file path names in the format: Last Name, First Name Policy_Number Month Annual Report.pdf
    First, this function reads the pdf, converts to jpeg format, uses optimal character recognition (OCR)
    to determine the text of the pdf document. This text is then searched using regular expressions for the
    necessary values including name, policy number and month. The file name is comprised accordingly
    :param filepath: path of the original pdf document - containing multiple annual reports
    :return: list of the valid save names of all reports in that document
    '''

    # Initiates list to Store save names of each individual page
    save_names = []

    # Split entire pdf document into its own page and analyze text
    pages = convert_from_path(filepath)
    for page in pages:
        print("Processing Page", page, "...")

        # save a jpeg to allow for easier OCR (optimal character recognition)
        page.save('out.jgp', 'JPEG')
        jpg_open = Image.open('out.jgp')
        output_text = image_to_string(jpg_open, lang='eng') # output OCR to string

        regex_buildr = regular_expressions.old_annual_regex()
        month = regex_buildr.find_month(output_text)+" "
        year = regex_buildr.find_year(output_text)+" "
        policy_no = regex_buildr.find_policyNo(output_text)+" "
        name = regex_buildr.find_name(output_text)+" "

        # CREATE FILE NAME
        path_name = name + policy_no + month + year + "Annual Statement.pdf"
        save_names.append(path_name) #append to path name
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

def init_new(path, is_test=False):
    '''
    Initializes the pdf processor: takes in the path of the original file, calls the new_file_name_generator() helper
    method in order to determine new file names. Splits the pdf document by each page and saves them
    :param path: the file path of the original document
    :return: none, generates n new files where n is the length of the pdf document
    '''
    # creates file names as per user's original requirements
    file_names = file_name_generator_new(path)
    fname = os.path.splitext(os.path.basename(path))[0]
    # print(file_names)

    # exit condition - unable to determine page count
    pages = 2

    # Generates location of save location for extracted files
    save_location = generate_save_location(is_test)

    # splits by page and saves the files to location
    pdf = PdfFileReader(path, strict=False)
    for page in range(0, pdf.getNumPages(), pages):
        if (page != "NONE"):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            pdf_writer.addPage(pdf.getPage(page+1))


            # select appropriate file name based on the generator
            output_filename = file_names[page//pages]

            # TODO: save to a user defined location
            # saves the file to the appropriate destination
            with open(save_location+output_filename, 'wb') as out:
                pdf_writer.write(out)

def init_old(path, is_test=False):
    '''
        Initializes the pdf processor: takes in the path of the original file, calls the new_file_name_generator() helper
        method in order to determine new file names. Splits the pdf document by each page and saves them
        :param path: the file path of the original document
        :return: none, generates n new files where n is the length of the pdf document
        '''
    # creates file names as per user's original requirements
    file_names = file_name_generator_old(path)
    fname = os.path.splitext(os.path.basename(path))[0]
    # print(file_names)

    # exit condition - unable to determine page count
    pages = 1

    # splits by page and saves the files to location
    pdf = PdfFileReader(path, strict=False)

    # Generates Save Location for Files
    save_location = generate_save_location(is_test)

    for page in range(0, pdf.getNumPages(), pages):
        if (page != "NONE"):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))

            # select appropriate file name based on the generator
            output_filename = file_names[page]

            # saves the file to the appropriate destination
            with open(save_location+output_filename, 'wb') as out:
                pdf_writer.write(out)




pytesseract.pytesseract.tesseract_cmd =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# times the process
# start_time = time.time()
# init_old("C:\\Users\\jmper\\Documents\\Scans\\2019-11-26_103051.pdf")
# init_old("test2.pdf")
# print("--- %s seconds ---" % (time.time() - start_time))


