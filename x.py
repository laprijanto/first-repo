import glob
import os
import xml.etree.ElementTree as et
from datetime import date, datetime
from glob import glob
from os import chdir
from time import ctime

import pandas as pd

# We can use dictionary comprehensions

etree = et.parse('C:/MyCode/xml/test-cdr.xml')
root = etree.getroot()

# number_of_records = int(root[len(root) - 1].text)
number_of_records = int(5)

df_call_data = pd.DataFrame()
df_a_party = pd.DataFrame()
df_b_party = pd.DataFrame()
df_a_adj = pd.DataFrame()
df_b_adj = pd.DataFrame()

csv_file_path = 'C:/MyCode/csv/'


def write_cdr_to_csv(filename, number_of_records, attrib_index=None):
    df = pd.DataFrame()  # initialised data
    data = {}  # initialised data

    for x in range(number_of_records):
        # Get attribute for all keys for different attribute index
        # Use directory comprehension
        if attrib_index is None:
            data.update({z: root[x].attrib[z] for z in root[x].keys()})
        else:
            data.update({z: root[x][attrib_index].attrib[z]
                         for z in root[x][attrib_index].keys()})
        # Create DF from those attributes and thier values
        df = df.append(
            pd.DataFrame.from_dict([data]), ignore_index=True)
    # Change columns' names
    if '_a_'in filename:
        df.columns = [y + '_a' for y in list(df.columns)]
    elif '_b_'in filename:
        df.columns = [y + '_b' for y in list(df.columns)]
    else:
        pass

    df.to_csv(f'{csv_file_path}{filename}', index=False)
    return df


def combined_csv_files(list_of_csv_files, file_out):
    # Consolidate all CSV files into one object
    df_cdr = pd.concat([pd.read_csv(file)
                        for file in list_of_csv_files], axis=1, sort=False)
    # Convert the above object into a csv file and export
    df_cdr.to_csv(file_out, index=False, encoding="utf-8")


df_call_data = write_cdr_to_csv('01_billing_call_data.csv', number_of_records)

df_a_party = write_cdr_to_csv(
    '02_billing_a_party.csv', number_of_records, attrib_index=int(0))

df_b_party = write_cdr_to_csv(
    '03_billing_b_party.csv', number_of_records, attrib_index=int(1))

df_a_adj = write_cdr_to_csv(
    '04_billing_a_adj.csv', number_of_records, attrib_index=int(2))

df_b_adj = write_cdr_to_csv(
    '05_billing_b_adj.csv', number_of_records, attrib_index=int(3))

# Change directory path
chdir(csv_file_path)
# print(os.getcwd())

# List all CSV files in the working dir
list_of_csv_files = [f for f in glob("*.csv")]

# Combined CSV files
file_out = "100_combined_cdr.csv"
combined_csv_files(list_of_csv_files, file_out)
