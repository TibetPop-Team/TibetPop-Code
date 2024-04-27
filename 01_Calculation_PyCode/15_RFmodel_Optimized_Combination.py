# _*_ coding:utf-8 _*_

import itertools
# Importing third-party libraries required for computation
import time
import numpy as np
import pandas as pd

# Building a decorator to calculate the execution time of a function
def print_execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        # Output the runtime of this module to a txt file
        txt = open('D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\py\\06combination_output.txt', 'w')
        txt.write('The RunTime of 06combination_output.py is ' + str(end_time - start_time) + '\n')
        print('success!')
    return wrapper

def combination(r2_dict, save_path):
    '''
    # Generate c(10,6) combinations of samples
    :param r2_dict: Dictionary containing R2 values of samples
    :param save_path: Path to save the information of sample combinations
    :return: None
    '''
    path = save_path + '\\' + 'combination.csv'
    file = open(path, 'w')
    # Build the header of the sample combination file
    title = 'No.' + ',' + 'A1' + ',' + 'A2' + ',' + 'A3' + ',' + 'A4' + ',' + 'A5' + ',' + 'A6' + ',' + 'AVG' + '\n'
    file.write(title)
    # Generate c(10,6) combinations
    combs = itertools.combinations(r2_dict.keys(), 6)
    # Combination serial number
    count = 1
    # Loop through all sample combinations
    for comb in combs:
        # Record the R2 of the current sample combination
        avg_list = []
        # Write the sample combination serial number to the file
        file.write(str(count) + ',')
        # Loop through all samples in the current sample combination
        for c in comb:
            avg_list.append(r2_dict[c])
            file.write(str(c + 1) + ',')
        # Calculate the average R2 of the current sample combination
        avg = np.array(avg_list).mean()
        file.write(str(avg) + '\n')
        count += 1
    file.close()
    data = pd.read_csv(path)
    # Calculate the average of R2 for all sample combinations
    data['E(AVG)'] = data['AVG'].mean()

    # Define an anonymous function to determine whether the R2 of a sample combination is greater than the average R2 of all sample combinations,
    # if greater, mark it as TRUE, otherwise as FALSE
    def assign(a, b):
        if a < b:
            return False
        else:
            return True

    data['FLAG'] = data.apply(lambda row: assign(row['AVG'], row['E(AVG)']), axis=1)
    data.to_csv(path, index=False)

def statistic(save_path):
    '''
    # Statistics of sample weight information
    :param save_path: Path to save sample weight information
    :return: None
    '''
    path = save_path + '\\' + 'combination.csv'
    # Define 10 variables to store the occurrences of each of the 10 samples
    count1, count2, count3, count4, count5, count6, count7, count8, count9, count10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    # Build a counting dictionary
    dic = {1: count1, 2: count2, 3: count3, 4: count4, 5: count5, 6: count6, 7: count7, 8: count8, 9: count9, 10: count10}
    data = pd.read_csv(path)
    # Select all sample combinations that meet the requirements
    tmp = data[data['FLAG'].isin([bool('True')])]
    field_list = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    # Loop through each field
    for field in field_list:
        tmp_list = tmp[[field]].values.tolist()
        # Count the occurrences of each sample in each column, 'elements' represent the samples, 'repeats' represent the frequency of each sample
        elements, repeats = np.unique(tmp_list, return_counts=True)
        # Construct a dictionary of samples and their frequencies
        data_dict = dict(zip(elements, repeats))
        # Loop through the dictionary of samples and their frequencies
        for key, value in data_dict.items():
            # Update the occurrences of each sample recorded in the dictionary
            dic[key] = dic[key] + value
    # Append the frequency of each sample and its corresponding sample occurrence to the csv file of sample combinations
    file = open(path, 'a')
    # Build the header information of the csv file
    header = 'No.' + ',' + 'Frequency' + ',' + 'ratio' + '\n'
    file.write(header)
    count = 0
    # Calculate the cumulative sum of the occurrences of each sample in all combinations
    for _, value in dic.items():
        count += value
    # Loop through the dictionary and write it to the csv file
    for key, value in dic.items():
        vector = str(key) + ',' + str(value) + ',' + str(value / count) + '\n'
        file.write(vector)
    file.close()

def zone(params_path, save_path):
    '''
    Combines samples into zones and calculates sample weight information.
    :param params_path: Path to save sample R2 information.
    :param save_path: Path to save sample combination and weight information.
    :return: None
    '''
    # Path to the optimal parameters
    path = params_path + '\\' + 'optimum_parameters' + '.csv'
    data = pd.read_csv(path)
    # Get sample R2
    r2_series = data['R2']
    # Convert sample R2 to a dictionary
    r2_dict = r2_series.to_dict()
    combination(r2_dict, save_path)
    statistic(save_path)
    print('success!!!')

@print_execute_time
def execute():
    '''
    :param: None
    :return: None
    '''
    # Zone names
    zoneID_list = ['zoneR01', 'zoneR02', 'zoneR03','zoneR04', 'zoneR05', 'zoneR06','zoneR07', 'zoneR08', 'zoneR09','zoneR10', 'zoneR11', 'zoneR12','zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    # Two groups for each zone
    for group in ['1', '2']:
        for zoneID in zoneID_list:
            # Path to store model parameters
            params_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zoneID + '\\01rf_param'
            # Path to store sample weights
            save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zoneID + '\\04weights'
            zone(params_path, save_path)

# Main function call
execute()