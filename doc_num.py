import enum

class doc_enum(enum.Enum):

    OLD = 1
    NEW = 2
    TERM = 3
    IDO = 4

def doc_to_string(num):
    TO_STRING = {
        1 : "Annual Statement.pdf",
        2 : "Annual Statement.pdf",
        3 : "Term Statement.pdf",
        4 : "IDO Letter.pdf"
    }

    return TO_STRING[num]



