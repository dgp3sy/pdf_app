from pytesseract import image_to_string
import pdf2image
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import time
import re
import os




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



def new_file_name_generator(filepath):
    '''
    Generates file path names in the format: Last Name, First Name Policy_Number Month Annual Report.pdf
    First, this function reads the pdf, converts to jpeg format, uses optimal character recognition (OCR)
    to determine the text of the pdf document. This text is then searched using regular expressions for the
    necessary values including name, policy number and month. The file name is comprised accordingly
    :param filepath: path of the original pdf document - containing multiple annual reports
    :return: list of the valid save names of all reports in that document
    '''

    # Defines Regular Expressions for finding following information
    month_findr = re.compile(r"(January | February | March | April | May | June | July | August | September | October | November | December)")
    policyNo_findr = re.compile(r"Policy No\. ([0-9/-]*)")
    name_findr = re.compile(r"Policyowner(.*?)(\n*?)ADVISOR_NAME_HERE ([A-Z _]*)")
    name_findr2 = re.compile(r"Policyholder:\n[A-Za-z ]*[0-9]*([A-Za-z ]*)")

    # Initiates list to Store save names of each individual page
    save_names = []

    # Split entire pdf document into its own page and analyze text
    pages = pdf2image.convert_from_path(filepath)
    for page in pages:

        # save a jpeg to allow for easier OCR (optimal character recognition)
        page.save('out.jgp', 'JPEG')
        jpg_open = Image.open('out.jgp')
        output_text = image_to_string(jpg_open, lang='eng') # output OCR to string

        # boolean flags to determine if item has been properly found in OCR string
        has_name = False
        has_month = False
        has_policy = False

        # placeholder for new file name values
        month="MONTH"
        policy_no="POLICY_NO"
        name="NAME"

        # set the month based on the regex established
        for match in month_findr.finditer(output_text):
            month = match.group(1)
            has_month = True
        # set the policy number based on regex established
        for match in policyNo_findr.finditer(output_text):
            policy_no = match.group(1)
            policy_no = policy_no.replace("-","")
            has_policy = True
        # set the name of the policy owner based on the regex established
        for match in name_findr.finditer(output_text):
            name = match.group(3)
            name = name.strip().replace("_","")
            name = prepare_name(name)
            has_name = True
        # if that name didnt work, try another possibilty for finding the appropriate name
        if (not has_name):
            for match in name_findr2.finditer(output_text):
                name = match.group(1)
                name = name.strip().replace("_", "")
                name = prepare_name(name)
                has_name = True

        # CREATE FILE NAME
        path_name = name + " " + policy_no + month + "Annual Statement.pdf"
        save_names.append(path_name) #append to path name
    return save_names

def init(path):
    '''
    Initializes the pdf processor: takes in the path of the original file, calls the new_file_name_generator() helper
    method in order to determine new file names. Splits the pdf document by each page and saves them
    :param path: the file path of the original document
    :return: none, generates n new files where n is the length of the pdf document
    '''
    # creates file names as per user's original requirements
    file_names = new_file_name_generator(path)
    fname = os.path.splitext(os.path.basename(path))[0]
    # print(file_names)

    # splits by page and saves the files to location
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        if (page != "NONE"):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))

            # select appropriate file name based on the generator
            output_filename = file_names[page]

            # TODO: save to a user defined location
            # saves the file to the appropriate destination
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)

        # printzx ('Created: {}'.format(output_filename))

# times the process
# start_time = time.time()
# init("whole_life.pdf")
# print("--- %s seconds ---" % (time.time() - start_time))

init("C:\\Users\\Danny Perkins\\PycharmProjects\\pdf_app\\Annual.pdf")