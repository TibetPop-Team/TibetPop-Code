# _*_ coding:utf8 _*_
# python2
# Programmer: Yancheng Li
# Compiled: April 20, 2022
# Contains 2 sub-modules: dissolve_11(), transform_12()
# Program Purpose: Obtain the Tibetan Human Settlement population grid: ths_pop
# Program Comments: Jinsong Liu
# Commented: July 9, 2022

# qtp represents "Qinghai-Tibet Plateau"
# al4 represents "administrative level 4 (township)"

# Import libraries
import arcpy
import sys
import time

# Accept control parameters passed in from the batch file using assignment statements
# param is the name of the file geodatabase, which is also its storage path
param = sys.argv[1]
# name is the abbreviation of the study area name, such as chn, qtp, etc.
# This prefix is related to the prefix of the dataset name inside the file geodatabase.
name = sys.argv[2]

# Set the output environment to overwrite output
arcpy.env.overwriteOutput = True
# Set the current workspace to param
arcpy.env.workspace = param
# Set the spatial reference coordinates of the qtp_al4_pop dataset as the coordinate system for the current environment output
arcpy.env.outputCoordinateSystem = arcpy.Describe(str(name)+'_al4_pop').spatialReference

# Use dissolve to further merge qtp_net_grid_identity and summarize the population count per grid
def dissolve_11():
    # Input dataset: qtp_net_grid_identity
    # Output dataset: qtp_net_grid_dissolve
    # Dissolve and summarize based on the FID_qtp_net field in qtp_net_grid_identity to generate the qtp_net_grid_identity dataset
    arcpy.Dissolve_management(str(name)+'_net_grid_identity', str(name)+'_net_grid_dissolve', ['FID_'+str(name)+'_net'], [['SUM_grid_pop', 'SUM']])
    print('Grid data merged!!!')

# Using the Feature to Raster command to output the contents of the SUM_SUM_grid_pop field in the qtp_net_grid_identity_dissolve dataset as the qtp_pop raster dataset
def transform_12():
    # Input dataset: qtp_net_grid_identity_dissolve
    # Output dataset: qtp_pop
    # Convert ***_net_grid_identity_dissolve to raster dataset sjz_pop based on the SUM_SUM_grid_pop field
    arcpy.FeatureToRaster_conversion(str(name)+'_net_grid_dissolve','SUM_SUM_grid_pop',str(name)+'_pop',1000)
    print('THS-POP data created!!!')
    # At this point, the dependent variable data for the TibetPop modelling, the THS-POP dataset, is completed

# Execute functions
def execute():
    start_time = time.time()
    dissolve_11()
    transform_12()
    print('THS-POP data creation completed!!!')
    print(time.time() - start_time)
    # Output the runtime of this module to qtp_process4.txt
    txt = open(str(name)+'_process4.txt','w')
    txt.write('The RunTime of Process4.py is '+ str(time.time() - start_time)+'\n')

# Main caller program
execute()