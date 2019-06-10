import tkinter as tk
from tkinter import filedialog as fd
import process_pdf


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
        self._entry = tk.Entry(self, textvariable=self.filepath)
        self._button = tk.Button(self, text="Browse...", command=self.browse)

    def _display_widgets(self):
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
    global files
    no_errors=True
    for each_file in files:
        try:
            process_pdf.init(each_file)
        except:
            no_errors=False
            print("ERROR: Unable to process file: ", each_file)
    if(no_errors):
        print("All files successfully processed!")

files = tuple()

root = tk.Tk()
filetypes = (
    ('Portable Document Format', '*.pdf'),
    ("All files", "*.*")
)
# change this to whatever you want to be the main directory for your search
file_browser = Browse(root, initialdir=r"C:\Users\student\Documents",
                      filetypes=filetypes)
# TODO: Selection of the specific file path rather than the root directory of this code
file_browser.pack(fill='x', expand=True)
submit_button = tk.Button(root, text="Submit", command=call_proccess_pdf)
submit_button.pack(fill='x')

root.mainloop()