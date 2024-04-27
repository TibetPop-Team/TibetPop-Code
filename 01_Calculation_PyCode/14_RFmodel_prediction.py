# _*_ coding:utf-8 _*_
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

# Importing third-party libraries required for computation
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Building a decorator to calculate the execution time of a function
def print_execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        # Output the runtime of this module to a txt file
        txt = open('D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\py\\05RFmodel_predict.txt', 'w')
        txt.write('The RunTime of 05RFmodel_predict.py is ' + str(end_time - start_time) + '\n')
        print('success!')
    return wrapper

def RFmodel_predict(sample_path, test_path, param_path, save_path, i):
    '''
    Predict population density in the Qinghai-Tibet Plateau.
    :param sample_path: Primary path storing training sample data.
    :param test_path: Primary path storing test sample data.
    :param param_path: Primary path storing model parameters.
    :param save_path: Primary path storing predicted population density results.
    :param i: Sample index.
    :return: None
    '''
    index_i = i - 1
    # Build the name of the file to output the importance of covariates
    importance_csv = save_path + '\\' + 'importance_covariate_' + str(i) + '.csv'
    file_importance = open(importance_csv, 'w')
    # 'imp' represents the covariates, which is a DataFrame. Convert it to a list and then to a string,
    # write it to the 'importance' file as the header of the file
    imp = pd.read_csv(sample_path)
    title_str = 'DEM' + ',' + 'LR' + ',' + 'SLP' + ',' + 'AMP' + ',' + 'AMT' + ',' + 'NDVI' + ',' + 'DTR' + ',' + 'SKD' + ',' + 'DTS' + ',' + 'TA' + '\n'
    file_importance.write(title_str)
    # Read the parameters required to build the model
    param = pd.read_csv(param_path)
    # Build the training model
    regr = RandomForestRegressor(oob_score=True, random_state=1)
    regr.set_params(n_estimators=int(param.loc[index_i, 'n_estimators']), max_features=int(param.loc[index_i, 'max_features']))
    # Train the model
    regr.fit(imp[['DEM', 'LR', 'SLP', 'AMP', 'AMT', 'NDVI', 'DTR', 'SKD', 'DTS', 'TA']].values, imp['THSPOP'].values)
    # Get the importance of covariates
    importance = regr.feature_importances_
    # Write the importance of each covariate to the file
    for k in range(len(importance)):
        file_importance.write(str(importance[k]) + ',')
    file_importance.close()
    # Save the predicted population density, write it to a txt file
    xypopGL_txt = save_path + '\\' + 'xypopGL_' + str(i) + '.txt'
    vector_csv = test_path
    data_predict = open(xypopGL_txt, 'w')
    # Read the test data
    data_covariate = pd.read_csv(vector_csv)
    m = 0
    covariate_line = data_covariate.loc[m, ['ROW', 'COLUMN', 'DEM', 'LR', 'SLP', 'AMP', 'AMT', 'NDVI', 'DTR', 'SKD', 'DTS', 'TA']]
    while True:
        # Predict for non-empty data
        if int(covariate_line['DTR']) >= 0:
            RFmodel_predict = regr.predict([covariate_line[['DEM', 'LR', 'SLP', 'AMP', 'AMT', 'NDVI', 'DTR', 'SKD', 'DTS', 'TA']].values])[0]
            outputstr = str(covariate_line['ROW']) + ',' + str(covariate_line['COLUMN']) + ',' + str(RFmodel_predict) + '\n'
            data_predict.write(outputstr)
        # Output empty values directly if they exist
        else:
            outputstr = str(covariate_line['ROW']) + ',' + str(covariate_line['COLUMN']) + ',' + str(covariate_line['DTR']) + '\n'
            data_predict.write(outputstr)
        m += 1
        # Reading the next line after reaching the last line of the file will raise an exception.
        # This exception handling will catch the exception and exit the loop.
        try:
            covariate_line = data_covariate.loc[m, ['ROW', 'COLUMN', 'DEM', 'LR', 'SLP', 'AMP', 'AMT', 'NDVI', 'DTR', 'SKD', 'DTS', 'TA']]
        except Exception:
            break
    data_predict.close()

@print_execute_time
def execute():
    '''
    Main function
    :param: None
    :return: None
    '''
    # Get the folder names storing training samples
    sample_name = ['spR01', 'spR02', 'spR03','spR04', 'spR05', 'spR06','spR07', 'spR08', 'spR09','spR10', 'spR11', 'spR12','spR13', 'spR14', 'spR15', 'spR16']
    # Get the names of parameter files
    zoneID = ['zoneR01', 'zoneR02', 'zoneR03','zoneR04', 'zoneR05', 'zoneR06','zoneR07', 'zoneR08', 'zoneR09','zoneR10', 'zoneR11', 'zoneR12','zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    for group in ['1', '2']:
        for sample, zone in zip(sample_name, zoneID):
            for i in range(1, 11):
                sample_path = 'D:\\QTP\\RF\\03final\\RF_5000\\03SP\\02sample_data' + '\\' + group + '\\' + sample + '\\' + 'sample_' + str(i) + '.csv'
                test_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zone + '\\02test' + '\\' + 'vector.csv'
                param_path = 'D:\\QTP\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zone + '\\01rf_param' + '\\' + 'optimum_parameters.csv'
                save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zone + '\\03predict'
                RFmodel_predict(sample_path, test_path, param_path, save_path, i)

# Main function call
execute()