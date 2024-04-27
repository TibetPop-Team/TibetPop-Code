# _*_ coding:utf-8 _*_
# qtp represents "Qinghai-Tibet Plateau"
# sp represents "sample"
# ssp represents "stratified sampling"
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

# Import third-party libraries for computation
import os
import time
import arcpy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Build a decorator to calculate execution time
def print_execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        # Write the runtime of this module to a txt file
        txt = open('D:\\QTP\\RF\\03final\\RF_5000\\03SP\\02sample_data\\01creategridsample.txt','w')
        txt.write('The RunTime of 01creategridsample.py is ' + str(end_time - start_time) + '\n')
        print('success!')
    return wrapper

def createGridsample(path, covariate_path, group, zoneID):
    '''
    Create grid training samples based on 5000 sampling point masks
    :param path: Path where the sampling data is stored
    :param covariate_path: Path where the covariate data is stored
    :param group: Sampling group
    :param zoneID: Zone identifier
    :return: None
    '''
    # Allow data to be overwritten
    arcpy.env.overwriteOutput = True
    # Set the workspace path
    arcpy.env.workspace = covariate_path
    # Read data and convert to arrays
    dem = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_dem.tif'))
    lr = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_lr.tif'))
    slp = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_slp.tif'))
    amp = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_amp.tif'))
    amt = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_amt.tif'))
    ndvi = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_ndvi.tif'))
    dtr = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_dtr.tif'))
    skd = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_skd.tif'))
    dts = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_dts.tif'))
    ta = arcpy.RasterToNumPyArray(arcpy.Raster('qtp_ta.tif'))
    thspop = arcpy.RasterToNumPyArray(arcpy.Raster('thspop.tif'))

    # Set the path of the sampling mask
    data_path = path + '\\01ssp\\ssp\\sp_mask\\' + group + '\\' + zoneID
    # Set the path to save the sampling data
    save_path = path + '\\02sample_data\\' + group + '\\' + zoneID
    arcpy.env.workspace = data_path
    samplecun_list = arcpy.ListRasters()
    # Loop through all the sampling mask data
    for sample in samplecun_list:
        s = arcpy.Raster(sample)
        s_array = arcpy.RasterToNumPyArray(s)
        # Build the training sample csv file
        path2 = save_path + '\\' + 'sample_' + sample.split('_')[1] + '.csv'
        # Open the training sample csv file in write mode
        with open(path2, 'w') as outputfile:
            # Build the header information of the training sample file
            title = 'id' + ',' + 'DEM' + ',' + 'LR' + ',' + 'SLP' + ',' + 'AMP' + ',' + 'AMT' + ',' + 'NDVI' + ',' + 'DTR' + \
                    ',' + 'SKD' + ',' + 'DTS' + ',' + 'TA' + ',' + 'RKMD' + '\n'
            outputfile.write(title)
            row = 0
            count = 0
            # Traverse the array composed of sampling masks row by row and column by column
            while row < s.height:
                col = 0
                while col < s.width:
                    # Get the covariate data corresponding to the sampling mask
                    if s_array[row, col] >= 1 and s_array[row, col] <= 50:
                        count += 1
                        vector = str(count) + ',' + str(dem[row, col]) + ',' + str(lr[row, col]) + ',' + str(slp[row, col]) + ',' + \
                                 str(amp[row, col]) + ',' + str(amt[row, col]) + ',' + str(ndvi[row, col]) + ',' + str(dtr[row, col]) + ',' + \
                                 str(skd[row, col]) + ',' + str(dts[row, col]) + ',' + str(ta[row, col]) + ',' + str(thspop[row, col]) + '\n'
                        outputfile.write(vector)
                    col += 1
                row += 1
    print('success!')

@print_execute_time
def execute_6():
    '''
    Main function
    :param: None
    :return: None
    '''
    # Path to sampling point mask
    path = 'D:\\QTP\\RF\\03final\\RF_5000\\03SP'
    # Path to covariate data
    covariate_path = 'D:\\QTP\\RF\\03final\\RF_5000\\01COVARIATE_DATA'
    # Sampling point mask names
    zoneID_list = ['spR01', 'spR02', 'spR03', 'spR04', 'spR05', 'spR06', 'spR07', 'spR08', 'spR09', 'spR10', 'spR11', 'spR12', 'spR13', 'spR14', 'spR15', 'spR16']
    # Group numbers
    for group in ['1', '2']:
        for zoneID in zoneID_list:
            createGridsample(path, covariate_path, group, zoneID)

# Main function call
execute_6()