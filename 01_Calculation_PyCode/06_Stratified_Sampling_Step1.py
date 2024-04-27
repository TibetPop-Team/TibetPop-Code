# _*_ coding:utf8 _*_
# strtf represents "stratified"
# ssp represents "stratified sampling"
# sp represents "sample"
# intvl represents "interval"

# Import necessary third-party libraries for computation
import os
import time
import arcpy
import sys

# Reload sys and set default encoding to 'utf-8'
reload(sys)
sys.setdefaultencoding('utf-8')

def notnull_count(array):
    '''
    Calculate the total number of non-null raster values within a certain zone
    :param array: The array form of raster data for population density within a certain zone
    :return: Total number of non-null raster values within a certain zone for population density
    '''
    cnt = 0
    row = 0
    # Loop through the rows of the array
    while row < array.shape[0]:
        col = 0
        # Loop through the columns of the array
        while col < array.shape[1]:
            # Record the total number of non-null values in the array
            if array[row][col] >= 0:
                cnt += 1
            col += 1
        row += 1
    return cnt

def count(array, m1, m2):
    '''
    Calculate the number of raster cells within a certain interval in a specific zone
    :param array: The array form of raster data for population density within a certain zone
    :param m1: The lower bound of the interval
    :param m2: The upper bound of the interval
    :return: The number of raster cells within a certain interval in a specific zone
    '''
    cnt = 0
    row = 0
    while row < array.shape[0]:
        col = 0
        while col < array.shape[1]:
            # The interval is left-closed and right-open
            if array[row][col] >= m1 and array[row][col] < m2:
                cnt += 1
            col += 1
        row += 1
    return cnt

def strtf_info_txt(strtf, save_path):
    '''
    Save stratified sampling information of different sampling scales into a txt file for later sampling
    :param strtf: A list of stratified sampling information for different sampling scales within a certain zone
    :param save_path: The path to save the stratified sampling information
    :return: None
    '''
    with open(save_path, 'w') as fp:
        for item in strtf:
            context = ','.join(item)
            fp.write(context)
            fp.write('\n')

def strtf_info_statistic_csv(intvl_name, n_list, strtf, save_path):
    '''
    Create a visualization table for stratified sampling, facilitating manual inspection
    :param intvl_name: The header information in the csv table
    :param n_list: A list of different sampling scales
    :param strtf: A list of stratified information corresponding to different sampling scales
    :param save_path: The path to save the stratified sampling information
    :return: None
    '''
    with open(save_path, 'w') as fp:
        fp.write(',' + intvl_name)
        for n, item in zip(n_list, strtf):
            context = str(n) + ',' + ','.join(item) + '\n'
            fp.write(context)

def strtf_info(strtf, n, array, mean, std, notnull_grid_count):
    '''
    Calculate the number of samples to be taken for each interval under a certain sampling scale
    :param strtf: The total list of stratified partition information for different sampling scales
    :param n: The sampling scale
    :param array: The array form of raster data for population density within a certain zone
    :param mean: The mean value
    :param std: The standard deviation
    :param notnull_grid_count: The number of non-null raster cells within a certain zone
    :return: The header information of a certain sampling scale, the content of which is the sampling interval
    '''
    strtf_list = []
    m1 = 0
    m2 = mean
    csv_title = str(m2) + ','
    cnt = n
    # Proportion of grid cells in a certain interval to the total grid cells within the zone
    intvl_ratio = round(count(array, m1, m2) / float(notnull_grid_count), 4)
    # Calculate the number of grid cells to be sampled within a certain interval under a certain sampling scale
    intvl_data_cnt = round(intvl_ratio * n)
    # Save the number of samples to be taken for the interval for subsequent stopping sampling conditions
    num_cnt = intvl_data_cnt
    # Save the sampling count to the list
    strtf_list.append(int(intvl_data_cnt))
    # Update the remaining number of samples to be taken
    cnt -= intvl_data_cnt
    while cnt > 0:
        # Calculate the upper and lower limits of the sampling interval
        m1 = m2
        m2 = m1 + std
        # Update the header information of the csv file
        csv_title = csv_title + str(m2) + ','
        intvl_ratio = round(count(array, m1, m2) / float(notnull_grid_count), 4)
        intvl_data_cnt = round(intvl_ratio * n)
        num_cnt += intvl_data_cnt
        # If the current sampling count is 0, add all the remaining sample counts to the current sample count to avoid having 0 samples in the sampling interval
        if intvl_data_cnt == 0:
            intvl_data_cnt = n - num_cnt
        strtf_list.append(int(intvl_data_cnt))
        cnt -= intvl_data_cnt
    res = sum(strtf_list)
    strtf_list = [str(i) for i in strtf_list]
    # Check if the total sampling count is consistent with the current sampling scale
    if res == n:
        strtf.append(strtf_list)
    else:
        raise Exception('Sampling total count error!')
    return csv_title[:-1] + '\n'

def sp_info(array, zoneID, mean, std, notnull_grid_count, save_path, sp_count):
    '''
    Calculate sampling statistics for different sampling scales
    :param array: The array form of raster data for population density within a certain zone
    :param zoneID: The zone name
    :param mean: The mean value
    :param std: The standard deviation
    :param notnull_grid_count: The number of non-null raster cells within a certain zone
    :param save_path: The path to save the stratified sampling information
    :param sp_count: A list of different sampling scales
    :return: None
    '''
    intvl_name = []
    strtf = []
    for cnt in sp_count:
        intvl_length = strtf_info(strtf, cnt, array, mean, std, notnull_grid_count)
        # Get the longest interval information for different sampling scales
        if len(intvl_length) > len(intvl_name):
            intvl_name = intvl_length
    path_txt = save_path + '\\' + str(zoneID) + '.txt'
    path_csv = save_path + '\\' + str(zoneID) + '.csv'
    # Execute sampling information functions
    strtf_info_txt(strtf, path_txt)
    strtf_info_statistic_csv(intvl_name, sp_count, strtf, path_csv)

def zone_info(data_path, save_path, zoneID, sp_count):
    '''
    Calculate sampling information for different sampling scales within a certain zone
    :param data_path: The path to population density data
    :param save_path: The path to save the stratified sampling information
    :param zoneID: The name of the zone
    :param sp_count: A list of sampling scales
    :return: None
    '''
    raster = arcpy.Raster(data_path)
    array = arcpy.RasterToNumPyArray(raster)
    mean = round(raster.mean, 2)
    std = round(float(arcpy.GetRasterProperties_management(raster, 'STD').getOutput(0)), 2)
    notnull_grid_count = notnull_count(array)
    sp_info(array, zoneID, mean, std, notnull_grid_count, save_path, sp_count)

def zone(data_path, save_path, zoneID_list, sp_count):
    '''
    Calculate sampling information for different sampling scales within different zones
    :param data_path: The path to population density data
    :param save_path: The path to save the stratified sampling information
    :param zoneID_list: A list of zone names
    :param sp_count: A list of sampling scales
    :return: None
    '''
    # Loop through all zones
    for zoneID in zoneID_list:
        data_path_new = data_path + '\\' + str(zoneID) + '.tif'
        save_path_new = save_path + '\\' + str(zoneID) + '_sp'
        folder = os.path.exists(save_path_new)
        if not folder:
            os.makedirs(save_path_new)
        zone_info(data_path_new, save_path_new, zoneID, sp_count)
        print(zoneID + ' stratified information has been written!!!')

def execute():
    '''
    Main function
    :param：None
    :return: None
    '''
    # Path to population density data for different zones
    data_path = 'D:\\RF\\03SP\\01ssp\\ssp\\thspop'
    # Path to save the stratified sampling information for different zones
    save_path = 'D:\\RF\\03SP\\01ssp\\ssp\\sp'
    # Mask names for the first group of zone sampling frames
    zoneID_list_1 = ['spR01', 'spR02', 'spR03', 'spR04']
    # Sampling scales for the first group
    sp_count_1 = [600]

    # Mask names for the second group of zone sampling frames
    zoneID_list_2 = ['spR05', 'spR06', 'spR07', 'spR08', 'spR09', 'spR10', 'spR11', 'spR12', 'spR13', 'spR14', 'spR15', 'spR16']
    # Sampling scales for the second group
    sp_count_2 = [5000]

    start_time = time.time()
    zone(data_path, save_path, zoneID_list_1, sp_count_1)
    zone(data_path, save_path, zoneID_list_2, sp_count_2)
    end_time = time.time()
    
    # Write the runtime of this module to a txt file
    txt = open('01strtf_1.txt','w')
    txt.write('The RunTime of 01strtf_1.py is ' + str(end_time - start_time) + '\n')

# Call the main function
execute()