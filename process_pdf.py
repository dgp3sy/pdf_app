import pytesseract
from pytesseract import image_to_string
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
import ido_reader
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

def file_name_generator_new(filepath):
    '''
    Generates file path names in the format: Last Name, First Name Policy_Number Month Annual Report.pdf
    First, this function reads the pdf, converts to jpeg format, uses optimal character recognition (OCR)
    to determine the text of the pdf document. This text is then searched using regular expressions for the
    necessary values including name, policy number and month. The file name is comprised accordingly
    :param filepath: path of the original pdf document - containing multiple annual reports
    :return: list of the valid save names of all reports in that document
    '''
    # month_findr = re.compile(r"(January | February | March | April | May | June | July | August | September | October | November | December)")
    date_findr = re.compile(r"through ([0-9]{2})/([0-9]{2})/([0-9]{4})")
    insured_findr = re.compile(r"Dean E Harder ([A-Za-z ]*)")
    insured_findr2 = re.compile(r"Dear ([A-Za-z ]*),")
    policyNo_findr_new = re.compile(r"(07[1|2][0-9]{7})")

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
        # boolean flags to determine if item has been properly found in OCR string
        found_name = False
        found_policy = False

        # placeholder for new file name values
        month = "MONTH "
        year = "YEAR "
        policy_no = "POLICY_NO "
        name = "NAME"
        # set the month based on the regex established
        for match in date_findr.finditer(text):
            month_num = int(match.group(1))
            month = prepare_month(month_num)+" "
            year = match.group(3)+" "

        # set the policy number based on regex established
        for match in policyNo_findr_new.finditer(text):
            policy_no = match.group(1)
            policy_no = policy_no.replace("-", "")

            # Add zero to certain policy numbers - user requirement
            policy_no = policy_no + " "
            found_policy = True

        # check to see if the policy is a new policy
        if not found_policy:
            for match in policyNo_findr_new.finditer(text):
                policy_no = match.group(1)
                found_policy = True

        # find the individual who is insured under the policy
        for match in insured_findr.finditer(text):
            name = match.group(1)
            name = name.strip().replace("-", "")
            name = prepare_name(name)
            found_name = True
        if not found_name:
            for match in insured_findr2.finditer(text):
                name = match.group(1)
                name = prepare_name(name)
                found_name = True
        # CREATE FILE NAME
        path_name = name + " " + policy_no + month + year + "Annual Statement.pdf"
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

    # Defines Regular Expressions for finding following information
    month_findr = re.compile(r"(January | February | March | April | May | June | July | August | September | October | November | December)")
    year_findr = re.compile(r"through [A-Za-z ]*[0-9]*, ([0-9]{4})")
    policyNo_findr_old = re.compile(r"Policy No\. ([0-9/-]*)")
    insured_findr = re.compile(r"which insures ([A-Za-z ]*)")

    # name_findr = re.compile(r"Policyowner(.*?)(\n*?)DEAN E HARDER ([A-Z _]*)")
    # name_findr2 = re.compile(r"Policyholder:\n[A-Za-z ]*[0-9]*([A-Za-z ]*)")

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

        # boolean flags for finding information
        found_policy = False

        # placeholder for new file name values
        month="MONTH "
        year = "YEAR "
        policy_no="POLICY_NO "
        name="NAME"

        # set the month based on the regex established
        for match in month_findr.finditer(output_text):
            month = match.group(1)

        # find the year
        for match in year_findr.finditer(output_text):
            year = match.group(1)+" "

        # set the policy number based on regex established
        for match in policyNo_findr_old.finditer(output_text):
            policy_no = match.group(1)
            policy_no = policy_no.replace("-","")
            found_policy = True

            # Add zero to certain policy numbers - user requirement
            policy_no = policy_no+"0"

        # check to see if the policy is a new policy
        if not found_policy:
            for match in policyNo_findr_old.finditer(output_text):
                policy_no = match.group(1)
        # find the individual who is insured under the policy
        for match in insured_findr.finditer(output_text):
            name = match.group(1)
            name = name.strip().replace("-","")
            name = prepare_name(name)

        # CREATE FILE NAME
        path_name = name + " " + policy_no + month + year + "Annual Statement.pdf"
        save_names.append(path_name) #append to path name
    return save_names
def init_new(path):
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


    # Get file path of desktop - extract to folder
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    save_location = desktop+"\\Extracted Pages\\"

    # manual override of save location here
    # save_location = "C:\\Users\\jmper\\Desktop\\Extracted Pages\\"

    if not os.path.exists(save_location):
        os.makedirs(save_location)


    # splits by page and saves the files to location
    pdf = PdfFileReader(path, strict=False)
    for page in range(0, pdf.getNumPages(), pages):
        if (page != "NONE"):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            pdf_writer.addPage(pdf.getPage(page+1))


            # select appropriate file name based on the generator
            output_filename = file_names[page]

            # TODO: save to a user defined location
            # saves the file to the appropriate destination
            with open(save_location+output_filename, 'wb') as out:
                pdf_writer.write(out)


def init_old(path):
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

    #### Edit Save Location Here ####

    # Get file path of desktop - extract to folder
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    save_location = desktop+"\\Extracted Pages\\"

    # manual override of save location here
    # save_location = "C:\\Users\\jmper\\Desktop\\Extracted Pages\\"

    # create folder if the path doesn't exist
    if not os.path.exists(save_location):
        os.makedirs(save_location)

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

