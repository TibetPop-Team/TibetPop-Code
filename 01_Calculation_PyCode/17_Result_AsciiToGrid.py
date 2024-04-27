# _*_ coding:utf8 _*_

import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.Describe('D:\\QTP\\RF\\03final\\RF_5000\\02MASK\\qtp_calc_mask.tif').SpatialReference

def execute():
    '''
    # Convert population density ascii files to raster
    :param: None
    :return: None
    '''
    # Zone names
    zoneID_list = ['zoneR01', 'zoneR02', 'zoneR03','zoneR04', 'zoneR05', 'zoneR06','zoneR07', 'zoneR08', 'zoneR09','zoneR10', 'zoneR11', 'zoneR12','zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    # Loop through groups
    for group in ['1', '2']:
        # Loop through zones
        for zoneID in zoneID_list:
            # Loop through samples
            for i in range(1, 11):
                # Population density ascii file
                data_path = 'D:\\QTP\\RF\\03final\\RF_5000\\05RESULT\\' + group + '\\' + zoneID + '\\01ascii\\' + 'popGL_' + str(i) + '.txt'
                # Raster save path
                save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\05RESULT\\' + group + '\\' + zoneID + '\\02grid\\' + zoneID + '_' + str(i) + '.tif'
                arcpy.ASCIIToRaster_conversion(data_path, save_path, 'FLOAT')
                print('success!')

# Main function call
execute()