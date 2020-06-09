# Annual Report Processor

Application to read scanned pdf documents of annual and quarterly report and prepare them for electronic filing. This is a project inspired by previous internship work in order to automate a process for companies in the future. Learn more about building this project by going to my [website](http://people.virginia.edu/~dgp3sy/python-processor.html).

## Getting Started
### Prerequisites

Make sure you have python 3.6, and install the following packages: PyPDF2, pytesseract, PyPDF2, PIL

In order to install dependent packages, cd into your project's location path and run the following commands in the terminal:
```
pip install pytesseract
```
```
pip install PyPDF2
```
```
pip install pytesseract
```
```
pip install PIL
```
Make sure that you have poppler and Tesseract-OCR added to your PATH. I found these resources helpful in doing this:
  * [Adding Poppler to PATH](https://github.com/QISKit/qiskit-terra/issues/586)
  * [Adding Tesseract-OCR to PATH](https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i/53672281)
  
## About the System
A detailed flowchart of the system proccess can be found below:
<img src="https://github.com/dgp3sy/pdf_app/blob/master/Flowchart.png">

## Deployment

This code is specific to a file structure, and uses regular expressions to search for data within that structure. If you would like to adapt this to your company's reports, please contact the author

## Authors

* **Dan Perkins**


## License

Copyright © 2019, [Dan Perkins](https://github.com/dgp3sy). All Rights Reserved

