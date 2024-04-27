# _*_ coding:utf-8 _*_
# qtp represents "Qinghai-Tibet Plateau"
# sp represents "sample"
# rf represents "random forest"
# dem represents "elevation"
# lr represents "land relief"
# slp represents "slope"
# amp represents "annual mean precipitation"
# amt represents "annual mean temperature"
# ndvi represents "Normalized Difference Vegetation Index"
# dtr represents "distance to river"
# skd represents "settlement kernel density"
# dts represents "distance to settlement"
# ta represents "transportation accessibility"
# thspop represents "Tibetan Human Settlement population grid, THS-POP"

# Importing necessary third-party libraries for computation
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from time import time

# Constructing a decorator to compute the execution time of a function
def print_execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        end_time = time()
        # Outputting the runtime of this module to a txt file
        txt = open('D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\py\\02parameters_selection.txt', 'w')
        txt.write('The RunTime of 02parameters_selection.py is ' + str(end_time - start_time) + '\n')
        print('success!')
    return wrapper

def parametersSelection(df, save_path, i):
    '''
    Calculate overall parameters for building a Random Forest model for population density prediction
    :param df: DataFrame to obtain training samples
    :param save_path: Path to save parameter information
    :param i: Index of training samples
    :return: None
    '''
    # Building the Random Forest model for population density
    regr = RandomForestRegressor(oob_score=True, random_state=1)
    # Getting predictor data
    x = df[['DEM', 'LR', 'SLP', 'AMP', 'AMT', 'NDVI', 'DTR', 'SKD', 'DTS', 'TA']]
    # Getting population density label data
    y = df['THSPOP']
    # Constructing a CSV file to record parameters
    path = save_path + '\\' + 'parameters_' + str(i) + '.csv'
    # Opening the CSV file to record parameters in write mode
    with open(path, 'w') as outputfile:
        # Building header information
        outputfile.write('n_estimators' + ',' + 'max_features' + ',' + 'R2' + '\n')
        # Setting the initial number of decision trees to 100
        i_count = 100
        # Setting the maximum number of decision trees to 500
        while i_count <= 500:
            # Setting the initial number of features to 2
            j_count = 2
            # Setting the maximum number of features to 10
            while j_count <= 10:
                # Setting parameters
                regr.set_params(n_estimators=i_count, max_features=j_count)
                # Fitting predictor data and population density label data
                regr.fit(x.values, y.values)
                # Getting the out-of-bag R2 score
                score = regr.oob_score_
                outputfile.write(str(i_count) + ',' + str(j_count) + ',' + str(score) + '\n')
                j_count += 1
            i_count += 10

def statistic_parameters(save_path, i):
    '''
    Calculate the optimal parameters for building a Random Forest model for population density prediction,
    Write n_estimators, max_features, and R2 parameters into corresponding CSV files
    to reduce the manual workload of copying data.
    :param save_path: Path to save parameter information
    :param i: Index of training samples
    :return: None
    '''
    path = save_path + '\\' + 'optimum_parameters' + '.csv'
    with open(path, 'a') as outputfile:
        title = 'n_estimators' + ',' + 'max_features' + ',' + 'R2' + '\n'
        if i == 1:
            outputfile.write(title)
        path2 = save_path + '\\' + 'parameters_' + str(i) + '.csv'
        data = pd.read_csv(path2)
        # Sort all data by R2 in descending order
        desc_data = data.sort_values(by='R2', ascending=False, inplace=False, ignore_index=True)
        # Extract the row with the maximum R2
        res = desc_data.iloc[[0]]
        # Convert data to a list
        res_list = res.values.tolist()
        # Construct the corresponding string and write it into the CSV file
        s = str(res_list[0][0]) + ',' + str(res_list[0][1]) + ',' + str(res_list[0][2]) + '\n'
        outputfile.write(s)

@print_execute_time
def execute():
    '''
    Main function
    :param: None
    :return: None
    '''
    # Set the path for storing training samples
    sample_path = 'D:\\QTP\\RF\\03final\\RF_5000\\03SP\\02sample_data'
    # Set the folder names for parameter saving
    sample_list = ['spR01', 'spR02', 'spR03', 'spR04', 'spR05', 'spR06', 'spR07', 'spR08', 'spR09', 'spR10', 'spR11', 'spR12', 'spR13', 'spR14', 'spR15', 'spR16']
    # Get the folder names where model parameters are stored
    file_list = ['zoneR01', 'zoneR02', 'zoneR03', 'zoneR04', 'zoneR05', 'zoneR06', 'zoneR07', 'zoneR08', 'zoneR09', 'zoneR10', 'zoneR11', 'zoneR12', 'zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    for group in ['1', '2']:
        for sample, file in zip(sample_list, file_list):
            save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + file + '\\01rf_param'
            for i in ['11']:
                df = pd.read_csv(sample_path + '\\' + group + '\\' + sample + '\\' + 'sample_' + str(i) + '.csv')
                parametersSelection(df, save_path, i)
                statistic_parameters(save_path, i)

# Caller function
execute()