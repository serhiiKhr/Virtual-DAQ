from tkinter import filedialog
import os

from .dw_reader import DWReader
from .mera_reader import MeraReader

FILES_EXTENSIONS = ['.mera', '.dxd']
def upload_file():
    path = filedialog.askopenfilename(filetypes=[("DW, MERA files", FILES_EXTENSIONS)])
    
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    
    if ext == ".dxd":
        reader = DWReader(filepath=path)
        return reader
    elif ext == ".mera":
        reader = MeraReader(filepath=path)
        return reader
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    