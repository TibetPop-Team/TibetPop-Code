# _*_ coding:utf8 _*_
# python2
# Programmer: Yancheng Li
# Compiled: April 20, 2022
# Contains 5 submodules: link_6(), identity_7(), field_8(), dissolve_9(), identity_10()
# Program Purpose: Obtain the Tibetan Human Settlement population grid: ths_pop
# Program Comments: Jinsong Liu
# Commented: July 9, 2022

# qtp represents "Qinghai-Tibet Plateau"
# al4 represents "administrative level 4 (township)"

# Importing libraries
import arcpy
import sys
import time

# Using assignment statements to receive control parameters passed in by the batch file
# param is the name of the file geodatabase and also its storage path
param = sys.argv[1]
# name is the abbreviation of the study area name, such as chn, qtp, etc.
# This prefix is related to the prefix of the dataset name inside the file geodatabase.
name = sys.argv[2]

# Set the output environment to overwrite mode
arcpy.env.overwriteOutput = True
# Set the current workspace to param
arcpy.env.workspace = param
# Set the spatial reference coordinates of the qtp_al4_pop dataset as the coordinate system for the current environment output
arcpy.env.outputCoordinateSystem = arcpy.Describe(str(name)+'_al4_pop').spatialReference

# Link the built-up area population to qtp_al4_built_spacejoin
def link_6():
    # Input dataset: qtp_al4_built_spacejoin
    # Input data file: qtp_built_pop.csv
    # Based on the id field, connect the calculated built-up area population, qtp_built_pop.csv, with ***_al4_built_spacejoin one by one.
    # Output dataset: qtp_built_pop. This is an important intermediate result dataset.

    # Create a layer named 'spacejoin' using qtp_al4_built_spacejoin
    arcpy.MakeFeatureLayer_management(str(name)+'_al4_built_spacejoin','spacejoin')
    # Join the two tables one by one using the OBJECTID_12 field in 'spacejoin' and the id field in qtp_built_pop.csv
    arcpy.AddJoin_management('spacejoin','OBJECTID_12_13',str(name)+'_built_pop.csv','id')
    # Output spacejoin as qtp_built_pop vector dataset, which is an important intermediate result dataset.
    arcpy.CopyFeatures_management('spacejoin',str(name)+'_built_pop')
    print('built-up area population attribute connection successful!!!')

# Use identity to overlay qtp_built_pop and qtp_net into one dataset: qtp_identity
def identity_7():
    # Input datasets: qtp_built_pop and qtp_net
    # Output dataset: qtp_identity
    # Use ***_net to identify ***_built_pop to obtain the grid ID corresponding to the built-up areas

    # Perform Identity spatial analysis
    arcpy.Identity_analysis(str(name)+'_built_pop',str(name)+'_net',str(name)+'_identity')
    print('Identification complete!!!')

# Add two new fields 'grid_area' and 'grid_pop' to the qtp_identity dataset and calculate field values
def field_8():
    # Input dataset: qtp_identity
    # Output dataset: qtp_identity
    # Program purpose: Add grid_area and grid_pop fields to qtp_identity and calculate their values

    # Add two fields
    arcpy.AddField_management(str(name)+'_identity', 'grid_area', 'DOUBLE')
    arcpy.AddField_management(str(name)+'_identity', 'grid_pop', 'DOUBLE')
    # Calculate the area value of grid_area, grid_area is the grid area value after being segmented by built-up areas
    arcpy.CalculateField_management(str(name)+'_identity','grid_area','!SHAPE.area!','PYTHON_9.3')
    # Utilize grid_area/?? *built_pop to obtain the population apportionment quantity of the patch
    arcpy.CalculateField_management(str(name)+'_identity','grid_pop','!grid_area! / !'+str(name)+'_built_pop_csv_built_area! * !'+str(name)+'_built_pop_csv_built_pop!','PYTHON_9.3')
    print('Field addition and calculation complete!!!')

# Use the FID_qtp_net field to dissolve qtp_identity and obtain a vector-format grid population dataset, and calculate the apportioned population quantity after dissolving
def dissolve_9():
    # Input dataset: qtp_identity
    # Output dataset: qtp_grid_pop
    # Based on the FID_qtp_net field in qtp_identity, dissolve qtp_identity, and by summing up, obtain the apportioned population count for grid cells
    arcpy.Dissolve_management(str(name)+'_identity',str(name)+'_grid_pop',['FID_'+str(name)+'_net'],[['grid_pop','SUM']])
    print('Grid data dissolving complete!!!')

# Use identity to overlay qtp_net and qtp_grid_pop, thereby enabling qtp_net to obtain the apportioned grid population count
def identity_10():
    # Input datasets: qtp_net and qtp_grid_pop
    # Output dataset: qtp_net_grid_identity
    # Use identity to overlay qtp_net and qtp_grid_pop, and output qtp_net_grid_identity, thereby enabling all grid cells to obtain the apportioned population count
    arcpy.Identity_analysis(str(name)+'_net',str(name)+'_grid_pop', str(name)+'_net_grid_identity')
    print('Identification complete!!!')

# Execute functions
def execute():
    start_time = time.time()
    link_6()
    identity_7()
    field_8()
    dissolve_9()
    identity_10()
    print('Preliminary data processing completed!!!')
    print(time.time() - start_time)
    # Output the runtime of this module to qtp_process3.txt
    txt = open(str(name)+'_process3.txt','w')
    txt.write('The RunTime of Process3.py is '+ str(time.time() - start_time)+'\n')

# Main calling program
execute()