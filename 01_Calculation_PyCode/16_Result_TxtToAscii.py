# _*_ coding:utf8 _*_

import arcpy
arcpy.env.overwriteOutput = True

def txtToascii(data_path, raster_path, save_path):
    '''
    # Convert predicted population density from txt to ascii format
    :param data_path: Path to the predicted population density txt file
    :param raster_path: Path to the zone mask raster
    :param save_path: Path to save the predicted population density in ascii format
    :return: None
    '''
    # Get raster dimensions
    desc = arcpy.Describe(raster_path)
    col, row = desc.width, desc.height
    # Get the lower-left corner coordinates of the raster
    left = int(arcpy.GetRasterProperties_management(raster_path, 'LEFT').getOutput(0))
    bottom = int(arcpy.GetRasterProperties_management(raster_path, 'BOTTOM').getOutput(0))
    inputfile = open(data_path, 'r')
    outputfile = open(save_path, 'w')
    # Build ascii header information
    outputfile.write('ncols         %d' % col + '\n')
    outputfile.write('nrows         %d' % row + '\n')
    outputfile.write('xllcorner     %d' % left + '\n')
    outputfile.write('yllcorner     %d' % bottom + '\n')
    outputfile.write('cellsize      1000' + '\n')
    outputfile.write('NODATA_value  -9999' + '\n')
    predict_line = inputfile.readline()
    while predict_line:
        line = predict_line.split(',')
        # Read column data
        c = int(float(line[1]))
        # Read predicted population density data
        predict = float(line[2])
        # Set to null value if predicted population density < 0
        if predict < 0:
            predict = -9999
        # Check if a new line is needed
        if c < col - 1:
            outputfile.write(str(predict) + ' ')
        else:
            outputfile.write(str(predict) + '\n')
        predict_line = inputfile.readline()
    outputfile.close()
    inputfile.close()

def execute_3():

    # zoneID names
    zoneID_name = ['zoneR01', 'zoneR02', 'zoneR03','zoneR04', 'zoneR05', 'zoneR06','zoneR07', 'zoneR08', 'zoneR09','zoneR10', 'zoneR11', 'zoneR12','zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    # Groups
    for group in ['1', '2']:
        for zoneID in zoneID_name:
            # Sample numbers
            for i in range(1, 11):
                # Population density prediction txt data
                data_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + zoneID + '\\03predict\\' + 'xypopGL_' + str(i) + '.txt'
                # zone raster data
                raster_path = 'D:\\QTP\\RF\\03final\\RF_5000\\02MASK\\' + zoneID + '.tif'
                # Population density prediction ascii data
                save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\05RESULT\\' + group + '\\' + zoneID + '\\01ascii\\' + 'popGL_'+ str(i) +'.txt'
                txtToascii(data_path, raster_path, save_path)
                print('success!')

# Main function call
execute_3()