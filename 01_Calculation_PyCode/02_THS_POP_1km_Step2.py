# python3.10.5
# Programmer: Yancheng Li
# Compiled: April 20, 2022
# Contains 1 sub-module: built_pop_5()
# Program Purpose: Use Pandas to calculate the population count of built areas, obtain the built-up area population table dataset: qtp_built_pop.csv
# Program Annotations: Jinsong Liu
# Commented: July 6, 2022

# qtp represents "Qinghai-Tibet Plateau"
# al4 represents "administrative level 4 (township)"

# Import libraries
import os
import sys
import time
import numpy as np
import pandas as pd

# Using assignment statements to receive control parameters passed in by the batch file
# param is the name of the file-type geodatabase and also its storage path
param = sys.argv[1]
# name is the abbreviation of the study area name, such as chn, qtp, etc.
# This prefix is related to the prefix of the dataset name inside the file-type geodatabase.
name = sys.argv[2]

# Calculate the population of built-up land using Pandas
def built_pop_5():
    
    # Calculate the population share of each piece of built-up land
    # Input file: qtp_al4_built_spacejoin.txt
    # Output file: qtp_al4_pop.csv
    
    # Read the text file of townships and built-up space join, and read it into the table
    table = pd.read_csv(os.path.join(param, str(name) + '_al4_built_spacejoin.txt'))
    # Get all column names from table and convert them to lowercase
    table.columns = table.columns.str.lower()
    # Summarize the built-up area corresponding to each township in the table using the groupby function,
    # and read it into built_area
    built_area = table.groupby('al4id').sum('built_area')['built_area'].rename('built_all_area')
    # Left join table with built_area based on the 'al4id' field, and read the left join result into new_table
    new_table = pd.merge(table, built_area, on='al4id', how='left')
    # Add the 'built_pop' field, and calculate its field values using the formula built_area / built_all_area * al4_pop
    new_table['built_pop'] = new_table['built_area'] / new_table['built_all_area'] * new_table['al4_pop']
    # Reset column index for new_table
    new_table = new_table.reindex(columns=['al4id', 'built_area', 'al4_area', 'built_all_area', 'al4_pop', 'built_pop'])
    # Set row index for new_table
    new_table.index = np.arange(1, len(new_table) + 1)
    # Save new_table as a csv file
    new_table.to_csv(os.path.join(param, str(name) + '_built_pop.csv'), index_label='id')
    print('Calculation of built-up land population completed!!!')

# Execute the function
def execute():

    # Record the starting time of the program execution
    start_time = time.time()
    built_pop_5()
    print(time.time() - start_time)
    # Output the runtime of this module to qtp_process2.txt
    txt = open(str(name) + '_process2.txt', 'w')
    txt.write('The RunTime of Process2 is ' + str(time.time() - start_time) + '\n')

# Main calling program
execute()