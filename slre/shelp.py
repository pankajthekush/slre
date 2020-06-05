
import tkinter as tk
from tkinter import filedialog
import os,sys,stat
from pathlib import Path

def browse_file_path(title_text="Choose File"):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes =(("Exe Files", "*.exe"),("All Files","*")),
                           title = title_text)
    return file_path


def copy_file_to(copyto,replace_file = False,title_text = 'Choose File'):
    already_exist = os.path.exists(copyto)
    if already_exist and not replace_file:
        print("Chrome driver already exists")
    else:
        c_driver = browse_file_path(title_text=title_text)
        cdriver = None
        with open(c_driver,'rb') as f:
            cdriver = f.read()
        with open(copyto,'wb') as f:
            f.write(cdriver)
        print(f'copied {c_driver} to {copyto}')
    
def copy_file_to_no_tk(copyto,replace_file = False,title_text = 'Choose File'):
    already_exist = os.path.exists(copyto)
    if already_exist and not replace_file:
        print("Chrome driver already exists")
    else:
        

        c_driver = os.path.join(str(Path.home()),'chromedriver')
        cdriver = None
        with open(c_driver,'rb') as f:
            cdriver = f.read()
        with open(copyto,'wb') as f:
            f.write(cdriver)
        print(f'copied {c_driver} to {copyto}')
        #chmod
        os.chmod(copyto, stat.S_IEXEC)





if __name__ == "__main__":
    copy_file_to_no_tk('chromedriver')
    
    

