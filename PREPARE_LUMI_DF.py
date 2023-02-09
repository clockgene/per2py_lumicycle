import pandas as pd
import numpy as np
import os
import datetime  as dt
from tkinter import filedialog
from tkinter import *

"""
Concatenate txt/csv files exported from Lumicycle Analysis by CTRL+SHIFT+T. Print mesors.
v.2023.02.09
"""

# Which column do you want to extract? Depends on Lumicycle Analysis version: 5 for v.2.6+, 4 for older versions. Plz check!
extract_column = 5

# Rename columns with traces to either original file name (1a_Raw,..., True) or to numbers so it works in per2py (1,2,..., False)
orig_filenames = True

# What is the delimiter format of the csv files? Comma or Semicolon?
delimiter = ','

# Set prefix for the output table, that will work as per2py input file
ID = 'LUMI'


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
    df2 = pd.read_csv(path+file, delimiter = delimiter, skiprows=[0, 1, 2], header=None, usecols=[extract_column - 1]) # CHOOSE , OR ; as delimiter, col 4 contains luminescence data
    if orig_filenames == True:
        df2.rename({extract_column - 1 : f'''{file.rsplit('.', 1)[0]}'''}, axis='columns', inplace=True)             #rename columns, using stackhack to extract filenam w/o ext
    else:
        df2.rename({extract_column - 1 : counter1}, axis='columns', inplace=True)     #rename columns to simple integers, for per2py to work w/o tinkering
    list_df.append(df2)
    counter1 += 1
df = pd.concat(list_df, axis = 1)                                                               #add all traces to 1 dataframe 
df.insert(0, 'TimesH', np.linspace(0, len(df.index)/6, num=len(df.index)))                  #create time column in hours, 10min/row
df.insert(1, 'Frame', df['TimesH']/1)  # may change this later to days or smthng
print(df.head())

print('Displaying the average/mesor/trend of extracted traces from time 0:-1,')
print('copy and paste to SUPER sheet:')
print()
mean_list = df.iloc[:-1, 2:].mean() #.mode().values
for i in mean_list:
    print(i)

# Save formated df as ID_signal.csv
df.to_csv(f'{path}{ID}_signal.csv', index=False)


"""
########## Stackhack subfolder-creation with timestamp ###########
mydir = os.path.join(os.getcwd(), dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(mydir)

"""
