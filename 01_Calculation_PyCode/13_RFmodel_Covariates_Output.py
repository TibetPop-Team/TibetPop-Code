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

# Import third-party libraries required for operations
import arcpy
import time

# Create a decorator to calculate the execution time of a function
def print_execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        # Output the runtime of this module to a txt file
        txt = open('D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\py\\04test_sample.txt', 'w')
        txt.write('The RunTime of 04test_sample.py is ' + str(end_time - start_time) + '\n')
        print('success!')
    return wrapper

def createVector(covariate_data):
    '''
    Convert the impact factor raster data extracted by zoning mask into a csv file.
    :param covariate_path: Primary path where impact factor data is stored.
    :return: None
    '''
    arcpy.env.workspace = covariate_data
    # Read all impact factor data into memory at once
    inRaster = arcpy.Raster('dem.tif')
    dem = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('dtr.tif')
    dtr = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('dts.tif')
    dts = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('skd.tif')
    skd = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('ndvi.tif')
    ndvi = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('amp.tif')
    amp = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('amt.tif')
    amt = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('lr.tif')
    lr = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('slp.tif')
    slp = arcpy.RasterToNumPyArray(inRaster)

    inRaster = arcpy.Raster('ta.tif')
    ta = arcpy.RasterToNumPyArray(inRaster)
    # Read the rows and columns of impact factors
    rows = dem.shape[0]
    cols = dem.shape[1]
    
    vector = covariate_data + '\\' + 'vector.csv'
    output = open(vector, 'w')
    # Build the header information of the test samples
    title_str = 'ROW' + ',' + 'COLUMN' + ',' + 'DEM' + ',' + 'LR' + ',' + 'SLP' + ',' + 'AMP' + ',' + 'AMT' + ',' + 'NDVI' + ',' + 'DTR' + ',' + 'SKD' + ',' + 'DTS' + ',' + 'TA' + '\n'
    output.write(title_str)
    # Loop through rows and columns
    row = 0
    while row < rows:
        col = 0
        while col < cols:
            vector_str = str(row) + ',' + str(col) + ',' + str(dem[row, col]) + ',' + \
                         str(lr[row, col]) + ',' + str(slp[row, col]) + ',' + str(amp[row, col]) + ',' + \
                         str(amt[row, col]) + ',' + str(ndvi[row, col]) + ',' + str(dtr[row, col]) + ',' + \
                         str(skd[row, col]) + ',' + str(dts[row, col]) + ',' + str(ta[row, col]) + '\n'
            output.write(vector_str)
            col += 1
        row += 1
    output.close()
    print('success!')

@print_execute_time
def execute():
    '''
    Main function
    :param：None
    :return: None
    '''
    # Set the names of zoning masks
    mask_list = ['zoneR01', 'zoneR02', 'zoneR03', 'zoneR04', 'zoneR05', 'zoneR06', 'zoneR07', 'zoneR08', 'zoneR09', 'zoneR10', 'zoneR11', 'zoneR12', 'zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    for group in ['1', '2']:
        for mask in mask_list:
            covariate_data = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + mask + '\\02test'
            createVector(covariate_data)
            print('success!')

# Main calling function
execute()