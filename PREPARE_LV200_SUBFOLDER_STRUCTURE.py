# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 13:21:49 2021
@author: Martin.Sladek
Creates structure of subdirectories for analysis of LV200 data
"""
import os, shutil
from tkinter import filedialog
from tkinter import *

# Desired name of the sample folder:
folderid = 'SCN'

# Desired names of the subregions (e.g. SCN Left and Right)
subregions = ['L', 'R']

# Desired names of the subfolders (e.g. SCN before and after treatment)
subdirectories = ['before', 'after']

# Total number of folders (e.g. analyzed SCNs)
total_no = 6

# Want specific sample names? Use custom list and comment out default list_of_samples
list_of_samples = [5,6]
#list_of_samples = range(1, total_no + 1)

##################### Tkinter button for browse/set_dir ################################
def browse_button():    
    global folder_path                      # Allow user to select a directory and store it in global var folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)
    sourcePath = folder_path.get()
    os.chdir(sourcePath)                    # Provide the path here
    root.destroy()                          # close window after pushing button

# Specify FOLDER BEFORE TREATMENT
root = Tk()
folder_path = StringVar()
lbl1 = Label(master=root, textvariable=folder_path)
lbl1.grid(row=0, column=1)
buttonBrowse = Button(text="Browse to parental folder", command=browse_button)
buttonBrowse.grid()
mainloop()
path = os.getcwd() + '\\'

newfolders = []
for directories in list_of_samples:
    for subregion in subregions:        
        for subdirectory in subdirectories:
            mydir_no = os.path.join(os.getcwd(), f'{folderid}{directories}{subregion}\\{subdirectory}')
            os.makedirs(mydir_no)        
            newfolders.append(mydir_no)
