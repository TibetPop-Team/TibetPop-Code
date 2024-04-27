# _*_ coding:utf8 _*_
# strtf represents "stratified"
# ssp represents "stratified sampling"
# sp represents "sample"

# Import necessary third-party libraries for computation
import time
import os
import arcpy
import sys

# Reload sys and set default encoding to 'utf-8'
reload(sys)
sys.setdefaultencoding('utf-8')

# Enable overwrite of output in arcpy environment
arcpy.env.overwriteOutput = True

def strtf_1(data_path_new, sp_path_new, strtf_path, zoneID):
    '''
    Create vector point stratified data
    :param data_path_new: Path to raster data of population density within a certain zone
    :param sp_path_new: Path to sampling data
    :param strtf_path: Path to save stratified data
    :param zoneID: Zone name
    :return: None
    '''
    raster = arcpy.Raster(data_path_new)
    mean = round(raster.mean, 2)
    std = round(float(arcpy.GetRasterProperties_management(raster, 'STD').getOutput(0)), 2)

    cnt = 0
    # Open the sampling file and count the number of intervals
    with open(sp_path_new + '\\' + str(zoneID) + '.txt', 'r') as fp:
        for i in fp:
            if len(i.split(',')) > cnt:
              cnt = len(i.split(','))
    name = strtf_path + '\\' + str(zoneID) + '_points'

    # Create folder for zone stratified data
    folder = os.path.exists(name)
    if not folder:
        os.makedirs(name)

    # Convert all raster data of the zone to vector point data
    arcpy.RasterToPoint_conversion(raster, name, 'VALUE')
    print('step1!')

    # Stratify the vector point data
    arcpy.MakeFeatureLayer_management(name + '.shp', 'pointlyr')
    n1 = 0
    n2 = mean
    for n in range(1, cnt+1):
        arcpy.SelectLayerByAttribute_management('pointlyr', 'NEW_SELECTION', '"grid_code">={} and "grid_code"<{}'.format(n1, n2))
        arcpy.CopyFeatures_management('pointlyr', name + '/points' + str(n))
        n1 = n2
        n2 = n1 + std
    print('step2!')

def execute_1(data_path, sp_path, strtf_path, zoneID_list):
    '''
    Create vector point data with different stratifications for different zones
    :param data_path: Path to population density data
    :param sp_path: Path to sampling data
    :param strtf_path: Path to save stratified data
    :param zoneID_list: List of zone names
    :return: None
    '''
    for zoneID in zoneID_list:
        data_path_new = data_path + '\\' + str(zoneID) + '.tif'
        sp_path_new = sp_path + '\\' + str(zoneID) + '_sp'
        strtf_1(data_path_new, sp_path_new, strtf_path, zoneID)
        print('Stratification completed!')

def execute_2():
    '''
    Main function
    :param：None
    :return: None
    '''
    # Path to population density data for different zones
    data_path = 'D:\\RF\\03SP\\01ssp\\ssp\\thspop'
    # Path to sampling data for different zones
    sp_path = 'D:\\RF\\03SP\\01ssp\\ssp\\sp'
    # Path to save original stratified data for different zones
    strtf_path = 'D:\\RF\\03SP\\01ssp\\ssp\\strtf'
    # Mask names for different zone sampling frames
    zoneID_list = ['spR01', 'spR02', 'spR03', 'spR04', 'spR05', 'spR06', 'spR07', 'spR08', 'spR09', 'spR10', 'spR11', 'spR12', 'spR13', 'spR14', 'spR15', 'spR16']
    start_time = time.time()
    execute_1(data_path, sp_path, strtf_path, zoneID_list)
    end_time = time.time()
    # Write the runtime of this module to a txt file
    txt = open('02strtf_2.txt', 'w')
    txt.write('The RunTime of 02strtf_2.py is ' + str(end_time - start_time) + '\n')

# Main function call
execute_2()