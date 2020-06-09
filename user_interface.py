import tkinter as tk
from tkinter import filedialog as fd
import process_pdf
import ido_reader
import time


class Browse(tk.Frame):
    """ Creates a frame that contains a button when clicked lets the user to select
    a file and put its filepath into an entry.
    """

    def __init__(self, master, initialdir='', filetypes=()):
        super().__init__(master)
        self.filepath = tk.StringVar()
        self._initaldir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._display_widgets()


    def _create_widgets(self):
        """
        creates the widgets for the User Interface: text entry and button
        """
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._button = tk.Button(self, text="Browse...", command=self.browse)

    def _display_widgets(self):
        '''
        displays widgets to user interface: text entry and button
        '''
        self._entry.pack(fill='x', expand=True)
        self._button.pack(anchor='se')

    def browse(self):
        """ Browses a .pdf file or all files and then puts it on the entry.
        """
        global files
        files = fd.askopenfilenames(initialdir=self._initaldir,
                                             filetypes=self._filetypes)
        files = root.tk.splitlist(files)
        self.filepath.set(files)
def call_proccess_pdf():
    """
    For each file selected in the browser UI, the system calls the init() function to process the file individually
    This function can be found in process_pdf.py and splits the file under specifications of page length and file name
    if there is an error, the file that was unable to be processed is notified to the user
    :return: None, although displays print to console if there is a successful job completed
    """
    global files
    global doc_type
    # output time for diagnostic purposes only - can be implemented by the user if desired
    # start_time = time.time()
    no_errors=True
    for each_file in files:
        try:
            # Document type determined by radio buttons:
            #   1 = New Annual Report
            #   2 = Old Annual Report
            #   3 = IDO Letter
            doc_type_int = doc_type.get()
            if doc_type_int == 1:
                process_pdf.init(each_file, is_old=False)
            elif doc_type_int == 2:
                process_pdf.init(each_file, is_old=True)
            elif doc_type_int == 3:
                ido_reader.init_ido_reader(each_file)
            else:
                raise
        except:
            no_errors=False
            print("ERROR: Unable to process file: ", each_file)
            raise
    if(no_errors):
        print("All files successfully processed!")
    # print("--- %s seconds ---" % (time.time() - start_time))

# initializes a tuple to hold all the file paths that the user selects
files = tuple()

# establishes the root tkinter for the UI
root = tk.Tk()
root.geometry("500x200") # sets the size of the UI window to 500px width by 200 px height

# defines the file types the user can search for - the purpose of this processor is mainly for pdfs
filetypes = (
    ('Portable Document Format', '*.pdf'),
    ("All files", "*.*")
)

# label for the UI
select_file_label = tk.Label(root, text="Select Report to Process:")

# change this to whatever you want to be the main directory for your search
file_browser = Browse(root, initialdir=r"C:\Users", filetypes=filetypes)

# defines the submit button to start the process, calls the function on every file passed through the file browser
submit_button = tk.Button(root, text="Submit", command=call_proccess_pdf)
# Determines the type of document with radio buttons
doc_type = tk.IntVar()
is_new = tk.Radiobutton(root, text="New Annual Report",
                          padx = 20, variable = doc_type,value = 1)
is_old = tk.Radiobutton(root, text="Old Annual Report",
                        padx = 20, variable = doc_type, value = 2)
is_IDO = tk.Radiobutton(root, text="IDO Letter",
                        padx = 20, variable = doc_type, value = 3)
# TODO: Selection of the specific file path rather than the root directory of this code

# Displays UI to the screen
select_file_label.pack()
file_browser.pack(fill='x', expand=True)
is_new.pack()
is_old.pack()
is_IDO.pack()
submit_button.pack(fill='x')
root.mainloop()