import tkinter as tk
from tkinter import filedialog as fd
import image_reader


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
        # self._button = tk.Button(self, text="Submit", command=image_reader.process_pdf())

    def _display_widgets(self):
        self._entry.pack(fill='x', expand=True)
        self._button.pack(anchor='se')

    def browse(self):
        """ Browses a .pdf file or all files and then puts it on the entry.
        """

        self.filepath.set(fd.askopenfilename(initialdir=self._initaldir,
                                             filetypes=self._filetypes))

root = tk.Tk()
filetypes = (
    ('Portable Document Format', '*.pdf'),
    ("All files", "*.*")
)
file_browser = Browse(root, initialdir=r"C:\Users",
                      filetypes=filetypes)

file_browser.pack(fill='x', expand=True)

root.mainloop()