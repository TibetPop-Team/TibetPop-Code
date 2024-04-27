# _*_ coding:utf8 _*_
# This step can be performed directly using software like ArcGIS for computation. The code is provided for reference only.

import arcpy
arcpy.env.overwriteOutput = True

def mosaic():
    '''
    # Mosaic the predicted population density raster data
    :param: None
    :return: None
    '''
    # Zone names
    zoneID_list = ['zoneR01', 'zoneR02', 'zoneR03','zoneR04', 'zoneR05', 'zoneR06','zoneR07', 'zoneR08', 'zoneR09','zoneR10', 'zoneR11', 'zoneR12','zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    # Loop through groups
    for group in ['1', '2']:
        # Construct a list to store raster paths
        raster_list = []

        zone_data_list = []

        # Path to save the mosaic
        save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\06MOSAIC\\' + group + '\\01calc'
        # Loop through zones
        for zoneID in zoneID_list:
            # Path to the population density prediction raster data with weighted combination for each zone
            data_path = 'D:\\QTP\\RF\\03final\\RF_5000\\05RESULT\\' + group + '\\' + zoneID + '\\03weight\\' + zoneID

            zone_data_list.append(data_path)
        zone_data = ';'.join(zone_data_list)
        print(zone_data)
        # Mosaic the rasters
        arcpy.MosaicToNewRaster_management(zone_data, save_path, 'qtp', cellsize=1000, number_of_bands=1)

mosaic()
