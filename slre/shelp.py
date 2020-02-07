
import tkinter as tk
from tkinter import filedialog
import os

def browse_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes =(("Exe Files", "*.exe"),("All Files","*.*")),
                           title = "Choose chromedriver.exe")
    return file_path


def copy_file_to(copyto,replace_file = False):
    already_exist = os.path.exists(copyto)
    if already_exist and not replace_file:
        print("Chrome driver already exists")
    else:
        c_driver = browse_file_path()
        cdriver = None
        with open(c_driver,'rb') as f:
            cdriver = f.read()
        with open(copyto,'wb') as f:
            f.write(cdriver)
        print(f'copied {c_driver} to {copyto}')
     



if __name__ == "__main__":
    copy_file_to(r"C:\Users\Pankaj\Documents\GitHub\slre\slre\54420\driver\chromedriver.exe")
    
    

