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

def createRandomPoints(path, num, numPoint, file, name):
    '''
    Extract the corresponding number of sampling points in each stratum
    :param path: Top-level path where data is stored
    :param num: Sampling scale
    :param numPoint: Stratified sampling numeric information
    :param file: Sampling group
    :param name: Zone name
    :return: None
    '''
    new_path = path + '/sp/' + str(name) + '_sp/' + str(num)
    folder = os.path.exists(new_path)
    if not folder:
        os.makedirs(new_path)
    new_path2 = new_path + '/samplepoints'
    folder = os.path.exists(new_path2)
    if not folder:
        os.makedirs(new_path2)
    new_path3 = new_path2 + '/' + str(file)
    folder = os.path.exists(new_path3)
    if not folder:
        os.makedirs(new_path3)
    arcpy.env.workspace = new_path
    outroute = new_path2 + '/' + str(file)
    for n in range(len(numPoint)):
        point = path + '/strtf/' + str(name) + '_points/' + 'points' + str(n+1) + '.shp'
        arcpy.CreateRandomPoints_management(outroute, 'points' + point.split('.')[0].split('/')[-1][6:], point, '', numPoint[n], 0, 'POINT', '')

def addField(path, num, n, file, name):
    '''
    Add the 'mask' field
    :param path: Top-level path where data is stored
    :param num: Sampling scale
    :param n: Index
    :param file: Sampling group
    :param name: Zone name
    :return: None
    '''
    for i in range(n):
        point = path + '/sp/' + str(name) + '_sp/' + str(num) + '/samplepoints/' + str(file) + '/points' + str(i+1) + '.shp'
        arcpy.AddField_management(point, 'mask', 'FLOAT')
        arcpy.CalculateField_management(point, 'mask', int(i+1))

def merge(path, num, file, name):
    '''
    Merge all stratified sampling points of the same zone
    :param path: Top-level path where data is stored
    :param num: Sampling scale
    :param file: Sampling group
    :param name: Zone name
    :return: None
    '''
    arcpy.env.workspace = path + '/sp/' + str(name) + '_sp/' + str(num) + '/samplepoints/' + str(file)
    outroute = path + '/sp/' + str(name) + '_sp/' + str(num) + '/samplepoints/' + str(file) + '/merge'
    folder = os.path.exists(outroute)
    if not folder:
        os.makedirs(outroute)
    point_list = []
    points = arcpy.ListFeatureClasses()
    for point in points:
        point_list.append(str(point))
    arcpy.Merge_management(point_list, outroute + '/' + 'merge')

def pointToRaster(path, calc_mask, num, file, name):
    '''
    Convert the merged sampling points to raster
    :param path: Top-level path where data is stored
    :param num: Sampling scale
    :param file: Sampling group
    :param name: Zone name
    :return: None
    '''
    arcpy.env.outputCoordinateSystem = arcpy.Describe(path + '/thspop/' + str(name) + '.tif').spatialReference
    arcpy.env.extent = calc_mask
    arcpy.env.mask = calc_mask
    point = path + '/sp/' + str(name) + '_sp/' + str(num) + '/samplepoints/' + str(file) + '/merge/merge.shp'
    outroute = path + '/sp_mask/'
    # Pay attention to the resolution of the raster
    arcpy.PointToRaster_conversion(point, 'mask', outroute + '/' + str(name), 'MOST_FREQUENT', '', 1000)

def execute_1(name, path, calc_mask):
    '''
    Get masks for different zones and sampling scales
    :param name: Zone name
    :param path: Top-level path where data is stored
    :param calc_mask: Study area mask
    :return: None
    '''
    num_list = ['5000']
    with open(path + '/sp/' + str(name) + '_sp/' + str(name) + '.txt') as fp:
        j = 0
        for row in fp:
            new_row = row.split(',')
            new_list = []
            for r in new_row:
                new_list.append(int(r))
            num = int(num_list[j])
            # Set the sampling frequency for training samples
            file = 1
            numPoint = new_list
            n = len(numPoint)
            createRandomPoints(path, num, numPoint, file, name)
            addField(path, num, n, file, name)
            merge(path, num, file, name)
            pointToRaster(path, calc_mask, num, file, name)

def execute_2():
    '''
    Main function
    :param: None
    :return: None
    '''
    # Zone sampling frame mask names
    fqmc_list = ['spR01', 'spR02', 'spR03', 'spR04', 'spR05', 'spR06', 'spR07', 'spR08', 'spR09', 'spR10', 'spR11', 'spR12', 'spR13', 'spR14', 'spR15', 'spR16']
    # Top-level path where stratified sampling information is stored
    path = 'D:\\RF\\03SP\\01SSP\\SSP'
    # Study area calculation mask data
    calc_mask = 'D:\\RF\\02MASK\\qtp_calc_mask.tif'
    start_time = time.time()
    for name in fqmc_list:
        execute_1(name, path, calc_mask)
        print('success!')
    end_time = time.time()
    # Write the runtime of this module to a txt file
    txt = open('03strtf_3.txt','w')
    txt.write('The RunTime of 03strtf_3.py is ' + str(end_time - start_time) + '\n')

# Main calling function
execute_2()