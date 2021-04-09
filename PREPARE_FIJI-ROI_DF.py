# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:07:56 2020
@author: Martin.Sladek
Create csv file from multiple FIJI ImageJ ROI tables, for per2py analysis
"""


import pandas as pd
import numpy as np
import glob, os
import datetime  as dt
from tkinter import filedialog
from tkinter import *


# Set prefix for per2py input file
ID = 'FIJI'


##################### Tkinter button for browse/set_dir ################################
def browse_button():    
    global folder_path                      # Allow user to select a directory and store it in global var folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)
    sourcePath = folder_path.get()
    os.chdir(sourcePath)                    # Provide the path here
    root.destroy()                          # close window after pushing button

root = Tk()
folder_path = StringVar()
lbl1 = Label(master=root, textvariable=folder_path)
lbl1.grid(row=0, column=1)
buttonBrowse = Button(text="Browse folder", command=browse_button)
buttonBrowse.grid()
mainloop()
 

"""
########## Return existing csv and other files in all subfolder of working folder, use in case of bugs 
for folderName, subfolders, filenames in os.walk('.\\'):
    for filename in filenames:
        print('FILE INSIDE ' + folderName + ': '+ filename)
"""

############# Prepare dataframe #######################################################
#######################################################################################

############# Prepare list of all csv files in work folder ############################
path = os.getcwd() + '\\'                     
filelist = [] 
for file in os.listdir(path):
    if file.endswith(".csv"):
        filelist.append(file)        

########## Prepare dataframe with all luminescence data from exported csv files ################                      
list_df = []
df = pd.DataFrame()
counter1 = 1
for file in filelist:
    df2 = pd.read_csv(path+file, delimiter = ',') #col 4 contains luminescence data  #, usecols=[1,2]
    #df2.rename({4 : f'''{file.rsplit('.', 1)[0]}'''}, axis='columns', inplace=True)             #rename columns, using stackhack to extract filenam w/o ext       
    df2.drop([' '], axis=1, inplace=True) #remove unnamed first columns with frames
    for i in df2.columns:
        df2.rename({i : counter1}, axis='columns', inplace=True)  #rename all columns to simple integers
        counter1 += 1    
    list_df.append(df2)
df = pd.concat(list_df, axis = 1)                                                               #add all traces to 1 dataframe    
df.insert(0, 'Frame', np.arange(len(df.index)))        #create time column in hours
df.insert(0, 'TimesH', df['Frame']/1)  # may change this later to days or smthng
print(df.head())

# Save formated df as ID_signal.csv
df.to_csv(f'{path}{ID}_signal.csv', index=False)


"""
########## Stackhack subfolder-creation with timestamp ###########
mydir = os.path.join(os.getcwd(), dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(mydir)

"""