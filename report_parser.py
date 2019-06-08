import PyPDF2

def pdf_split(file_name, splits):
    pdfFileObj = open(file_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    #starting index of first slice
    start = 0
    end = splits[0]

    for i in range(len(splits) + 1):
        # creating pdf writer object for (i+1)th split
        pdfWriter = PyPDF2.PdfFileWriter()

        # TODO : extract account number from pdf file
        account_number = i

        # output pdf file name
        outputpdf = file_name.split('.pdf')[0] + str(account_number) + '.pdf'

        # adding pages to pdf writer object
        for page in range(start, end):
            pdfWriter.addPage(pdfReader.getPage(page))

            # writing split pdf pages to pdf file
        with open(outputpdf, "wb") as f:
            pdfWriter.write(f)

            # interchanging page split start position for next split
        start = end
        try:
            # setting split end position for next split
            end = splits[i + 1]
        except IndexError:
            # setting split end position for last split
            end = pdfReader.numPages

            # closing the input pdf file object
    pdfFileObj.close()