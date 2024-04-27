# _*_ coding:utf8 _*_

import arcpy
import numpy as np

arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.Describe('D:\\QTP\\RF\\03final\\RF_5000\\02MASK\\qtp_calc_mask.tif').SpatialReference

def weight_map(zoneID, raster_path, weight_path, mask_path, save_path):
    '''
    # Calculate sample weights
    :param zoneID: Zone name
    :param raster_path: Path to population density prediction raster data
    :param weight_path: Path to sample weight file
    :param mask_path: Path to zone mask
    :param save_path: Path to save the raster after combining sample weights
    :return:
    '''
    path = weight_path + '\\' + 'combination.csv'
    map_weight = open(path , 'r')
    weight_list = []
    # Reposition file pointer
    for _ in range(212):
        map_weight.readline()
    # Get sample weights
    for _ in range(10):
        weight = float(map_weight.readline().strip().split(',')[-1])
        weight_list.append(weight)

    raster_list = []
    # Loop through raster data of zone groups
    for i in range(1, 11):
        raster = raster_path + '\\' + zoneID + '_' + str(i) + '.tif'
        raster_list.append(raster)
    # Create an empty array with the same extent as the zone mask
    array = np.zeros(arcpy.RasterToNumPyArray(mask_path).shape)
    # Combine weights
    for raster, weight in zip(raster_list, weight_list):
        array += arcpy.RasterToNumPyArray(raster) * weight
    left = arcpy.GetRasterProperties_management(mask_path, 'LEFT').getOutput(0)
    bottom = arcpy.GetRasterProperties_management(mask_path, 'BOTTOM').getOutput(0)
    grid = arcpy.NumPyArrayToRaster(array, arcpy.Point(left, bottom), 1000, 1000, array[0][0])
    grid.save(save_path + '\\' + zoneID)
    print('success!')

def execute():
    # Zone names
    zoneID_list = ['zoneR01', 'zoneR02', 'zoneR03','zoneR04', 'zoneR05', 'zoneR06','zoneR07', 'zoneR08', 'zoneR09','zoneR10', 'zoneR11', 'zoneR12','zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    # Loop through groups
    for group in ['1', '2']:
        # Loop through zones
        for zoneID in zoneID_list:
            # Path to population density prediction raster data
            raster_path = 'D:\\QTP\\RF\\03final\\RF_5000\\05RESULT\\' + group + '\\' + zoneID + '\\' + '\\02grid'
            # Path to sample weight
            weight_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zoneID + '\\' + '\\04weights'
            # Zone mask
            mask_path = 'D:\\QTP\\RF\\03final\\RF_5000\\02MASK\\' + zoneID + '.tif'
            # Path to save raster data after weight combination
            save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\05RESULT\\' + group + '\\' + zoneID + '\\' + '\\03weight'
            weight_map(zoneID, raster_path, weight_path, mask_path, save_path)

# Main function call
execute()