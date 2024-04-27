# -*- coding: utf-8 -*-
# Version: Python 2.7.3
# Purpose: Create a study area mask, laying the groundwork for subsequent calculation mask and other processing.
# Authors: Yancheng Li, Peizhang Wen, Yi Liu
# Date: December 1, 2021
# Revised date: November 27, 2021
# Description: Build a fishnet based on vector boundaries, add fields, select grids based on natural boundary location, then convert to raster to generate a mask.
# Requirements: Determine the number of rows and columns of the fishnet based on the approximate extent of the study area beforehand.

# qtp represents "Qinghai-Tibet Plateau"
# nb represents "natural boundary of qtp"

# Import arcpy and sys (system files) modules
import arcpy
import sys

# Reset encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Check if the number of blocks created by the fishnet meets the requirement. 
# If the fishnet exceeds 2GB, an error will occur, so it's necessary to divide a large study area into rows and columns.
def input_r_c(row, col, r, c):
    '''
    Divide the rows and columns of the entire fishnet into blocks, and check if they can be evenly divided to ensure that the boundaries of each divided fishnet do not overlap.
    :param row: The number of rows of the entire fishnet after processing.
    :param col: The number of columns of the entire fishnet after processing.
    :param r: The number of rows divided manually.
    :param c: The number of columns divided manually.
    :return:
    '''	

    # Check if the number of rows of the entire fishnet after processing can be evenly divided by the number of rows divided manually.
    if row % r == 0:

        # Check if the number of columns of the entire fishnet after processing can be evenly divided by the number of columns divided manually.
        if col % c == 0:

            # If both rows and columns can be evenly divided, the divided rows and columns are appropriate.
            return 'The division of blocks is appropriate!'

    # Instantiate an exception, and if the above conditions are not met, raise this exception.
    ex = Exception('The division of blocks is not appropriate!')

    # If they cannot be evenly divided, raise an error, and it's necessary to re-determine the number of rows and columns.
    raise ex

# Create Fishnet
def create_fishnet(fishnet1, left1, right1, top1, bottom1):
    '''
    Create a fishnet
    :param fishnet1: The path to save the fishnet
    :param left1: Leftmost coordinate of the fishnet
    :param right1: Rightmost coordinate of the fishnet
    :param top1: Topmost coordinate of the fishnet
    :param bottom1: Bottommost coordinate of the fishnet
    :return:
    '''

    # Output feature class for the fishnet
    outFeatureClass = fishnet1

    # Set the origin of the fishnet
    originCoordinate = str(left1) + ' ' + str(bottom1)

    # Set the orientation
    yAxisCoordinate = str(left1) + ' ' + str(bottom1 + 10)

    # Enter 100 for width and height of the fishnet
    cellSizeWidth = '100'
    cellSizeHeight = '100'

    # Automatically calculate the number of rows and columns based on the specified range and pixel size
    numRows = ''    
    numColumns = ''

    # Diagonal of the fishnet set by X and Y coordinate values. 
    # If a template extent is used, the value of the diagonal will be set automatically. 
    # This parameter will be disabled if origin, Y-axis, cell size, and number of rows and columns are set.
    oppositeCoorner = str(right1) + ' ' + str(top1)

    # Do not create point label feature class
    labels = 'NO_LABELS'

    # Range set by origin and diagonal
    templateExtent = ''

    # Define each output cell as a polygon
    geometryType = 'POLYGON'

    # Create the fishnet
    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns, oppositeCoorner, labels, templateExtent, geometryType)
    
    # Print the progress, indicating successful creation of the fishnet
    print('success!!!')

# Define the boundaries of the fishnet
def boundary_fishnet(fishnet, r, c):
    '''
    Determine the boundaries of the segmented fishnet
    :param fishnet: Folder to store the fishnet
    :param r: Number of rows artificially divided
    :param c: Number of columns artificially divided
    :return:
    '''

    # Get the attribute information of the vector data
    desc = arcpy.Describe(raw_input)

    # Process the boundaries of the fishnet so that the last four digits are 0000
    left = int(desc.extent.XMin) // 100000 * 100000
    bottom = int(desc.extent.YMin) // 100000 * 100000
    right = int(desc.extent.XMax) // 100000 * 100000 + 100000
    top = int(desc.extent.YMax) // 100000 * 100000 + 100000

    # Print the boundaries of each fishnet
    print(left, right, top, bottom)

    # Output how many rows and columns the fishnet has
    row = (top - bottom) // 100
    col = (right - left) // 100
    print(row, col)

    # Check whether the artificially divided rows and columns can be evenly divided by the rows and columns of the entire fishnet
    try:
        res = input_r_c(row, col, r, c)
        print(res)

    # If the above conditions are not met, print the set information and exit the program
    except Exception as result:
        print(result)
        sys.exit()

    # Calculate the boundaries of the segmented fishnet
    row1 = (top - bottom) / r
    col1 = (right - left) / c
    count1 = left - col1
    count2 = top + row1
    num = 0
    for i in range(r):
        count2 -= row1
        for j in range(c):
            num += 1
            count1 += col1
            left1 = int(count1)
            right1 = int(count1 + col1)
            top1 = int(count2)
            bottom1 = int(count2 - row1)
            fishnet1 = fishnet + '/' + 'fishnet'+str(num) + '.shp'
            create_fishnet(fishnet1, left1, right1, top1, bottom1)
            # Print the calculated boundaries of the segmented fishnet
            print(left1, right1, top1, bottom1)
        count1 = left - col1

# Define a function to add fields to the fishnet
def addField(fishnet):

    # Set the working environment to the path of the fishnet, i.e., the path where the fishnet is generated
    arcpy.env.workspace = fishnet

    # Get a list of fishnet feature classes
    fishnet_list = arcpy.ListFeatureClasses()

    # Iterate through the list of feature class names, net is the name of the dataset pointed to by the current loop pointer
    for net in fishnet_list:

        # Add a 'mask' field to the feature class
        arcpy.AddField_management(net, 'mask', 'FLOAT')

        # Update the values of the 'mask' field in the feature class
        arcpy.CalculateField_management(net, 'mask', 1)

    # Print the progress, indicating successful addition of fields
    print('addField success!!!')

# Define the polygon to raster conversion function
def polygontoraster(fishnet, mask):

    # Set the working environment to the path of the fishnet, i.e., the path where the fishnet is generated
    arcpy.env.workspace = fishnet
    fishnet_list = arcpy.ListFeatureClasses()
    for net in fishnet_list:
        arcpy.MakeFeatureLayer_management(net, 'fishnet_lyr')
        arcpy.SelectLayerByLocation_management('fishnet_lyr', 'intersect', raw_input)
        arcpy.CopyFeatures_management('fishnet_lyr', fishnet[:-4] + '2mask/' + net.split('.')[0][4:])
        inFeatures = 'fishnet_lyr'
        valField = 'mask'
        outRaster = mask + '/' + net.split('.')[0]
        assignmentType = 'CELL_CENTER'
        priorityField = 'NONE'
        cellSize = 100
        arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
        #arcpy.FeatureToRaster_conversion(inFeatures, valField, outRaster, cellSize)

    print('polygontoraster success!!!')

# Define the mosaic function
def mosaic(mask, mask_name):

    # Set the working environment to the path of the mask, i.e., the path where the mask is generated
    arcpy.env.workspace = mask
    list_label = []
    rasters = arcpy.ListRasters()
    for raster in rasters:
        list_label.append(raster)
    list_label = ';'.join(list_label)
    arcpy.MosaicToNewRaster_management(list_label, mask, mask_name, cellsize=1000, number_of_bands=1)
    print('mosaic success!!!')

# Define the main function
def execute(fishnet, mask, r, c, mask_name):

    # Execute the function to determine the boundaries of the fishnet
    boundry_fishnet(fishnet, r, c)

    # Execute the function to add fields to the fishnet
    addField(fishnet)

    # Execute the polygon to raster conversion
    polygontoraster(fishnet, mask)

    # Execute the mosaic function
    mosaic(mask, mask_name)

# Main program
if __name__ == '__main__':

    # Set environment settings for overwrite mode
    arcpy.env.overwriteOutput = True

    # Path to the original vector data
    raw_input = 'D:/QTP/qtp_nb.shp'
    raw_input_prj = 'D:/QTP/qtp_nb.prj'

    # Path to save the generated fishnet
    fishnet = 'D:/QTP/mask/1net'

    # Path to save the generated mask
    mask = 'D:/QTP/mask/2mask'

    # Add spatial projection
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(raw_input_prj)

    # Number of rows and columns for partitioning (8 rows, 6 columns, creating a total of 48 fishnets)
    r = 8
    c = 6

    # Name of the merged partition mask
    mask_name = 'nb_mask'

    # Execute the main function
    execute(fishnet, mask, r, c, mask_name)

    # Print whether the final progress is completed
    print('all success!!!')