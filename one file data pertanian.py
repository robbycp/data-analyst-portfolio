import pandas as pd
import os

def name_header(file_name):
    '''
    split file_name into list of strings
    '''
    name = file_name.split('_')
    del name[-3:]
    return name

def change_format_data(file_name):
    '''
    Change the format of the data to the format that ready to analyze
    :param file_name: csv filename
    :return: dataframe ready to concatenate and list of name strings
    '''
    df = pd.read_csv(file_name, index_col=[1])
    del df['Unnamed: 0']  # hapus yg ga perlu
    df = df.T  # transpose tabel
    df = df.reset_index()
    df = df.rename(columns={'index': 'Tahun'})
    new_name = []
    name = name_header(file_name)
    for i in range(0, len(name), 2):  # make a list of two, consist of name header from the file name.
        new_name.append([name[i], name[i + 1]])
    i = 0
    for cat, val in new_name:  # add variable name header into column in table
        df.insert(i, cat, val)
        i += 1
    # test output
    #print df
    return df, name

def concatenate_data(next_filename, prev_data):
    '''
    concatenate dataframe produced in change_format_data
    :param next_filename: next file to change the format and concatenate
    :param prev_data: dataframe from all concatenated dataframe
    :return: dataframe
    '''
    new_data, header = change_format_data(next_filename)
    data = pd.concat([prev_data, new_data])
    if 'Nasional' in header:
        important = ['Sub Sektor', 'Indikator', 'Level', 'Status Angka', 'Tahun']
    elif 'Provinsi' in header:
        important = ['Sub Sektor', 'Indikator', 'Level', 'Provinsi', 'Status Angka', 'Tahun']
    reordered = important + [c for c in data.columns if c not in important]
    data = data[reordered]
    return data

# Making a list of file name
path_old_file = r'E:\hortikultur\\'     # where all csv files
all_name_file = []
for file in os.listdir(path_old_file):
    if file.endswith(".csv"):
        all_name_file.append(file)

# Concantenate all data into one dataframe
pathf = r'E:\hortikultur\jadisatu\\'    # Path to save the file
data = pd.DataFrame()
iter = 1
list_satuan = []
for i in range(0, len(all_name_file)):
    data = concatenate_data(all_name_file[i], data)
    print "%s data succeed" % iter
    iter += 1

# Save dataframe to csv
filename = "Hortikultura.csv"
data.to_csv(pathf + filename)

''' One file testing
name = 'Sub Sektor_Hortikultura_Indikator_Luas Panen_Level_Nasional_Status Angka_Status Saat Ini_Tahun_1960-1969_.csv'
df = pd.DataFrame()
data = change_format_data(name)
#data.to_csv(r'E:\hortikultur\format lama\\'+name)
print data
print data.columns.values
print data.index.values
'''