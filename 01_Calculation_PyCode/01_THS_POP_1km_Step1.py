# _*_ coding:utf8 _*_
# python2.7.2
# Programmer: Yancheng Li
# Compiled: April 20, 2022
# Contains 3 submodules: addField_Calcul_2(), spacejoin_3(), exportTable_4()
# Program Purpose: Generate qtp_built_spacejoin.txt
# Program Comments: Jinsong Liu
# Commented: July 6, 2022

# qtp represents "Qinghai-Tibet Plateau"
# al4 represents "administrative level 4 (township)"

# Import function libraries
import arcpy
import sys
import time

# Use assignment statements to receive control parameters passed in by batch file
# param is the name of the file geodatabase and its storage path
param = sys.argv[1]
# name is the abbreviation of the study area name, such as chn, qtp, etc.
# This prefix is related to the prefix of the dataset name inside the file geodatabase.
name = sys.argv[2]

# Set the output environment to overwrite output mode
arcpy.env.overwriteOutput = True
# Specify the current workspace as param
arcpy.env.workspace = param
# Use the spatial reference coordinates of the qtp_al4_pop dataset as the coordinate system for current environment outputs
arcpy.env.outputCoordinateSystem = arcpy.Describe(str(name)+'_al4_pop').spatialReference

# Calculate township area
def addField_Calcul_2():

    # Add the AREA field in the qtp_al4_pop dataset and calculate the township area values
    # Input dataset: qtp_al4_pop
    # Output dataset: qtp_al4_pop
    
    # Add AREA fields
    arcpy.AddField_management(str(name) + '_al4_pop', 'AL4_AREA', 'DOUBLE')
    arcpy.AddField_management(str(name) + '_built', 'BUILT_AREA', 'DOUBLE')
    # Calculate values for AREA fields
    arcpy.CalculateField_management(str(name) + '_al4_pop', 'AL4_AREA', '!shape.geodesicArea@METERS!', 'PYTHON_9.3')
    arcpy.CalculateField_management(str(name) + '_built', 'BUILT_AREA', '!shape.geodesicArea@METERS!', 'PYTHON_9.3')
    print('Area fields added and calculated!!!')

# Perform a spatial join to assign each built-up area polygon its corresponding township code
def spacejoin_3():
    
    # target_features: qtp_built
    # join_features: qtp_al4_pop
    # Input datasets: qtp_built, qtp_al4_pop
    # Output dataset: qtp_al4_built_spacejoin, or out_feature_class
    
    # Spatially join qtp_built with qtp_al4_pop to assign each built-up area polygon its corresponding township code
    arcpy.SpatialJoin_analysis(str(name) + '_built', str(name) + '_al4_pop', str(name) + '_al4_built_spacejoin', match_option='WITHIN')
    print('Obtaining township codes for built-up areas!!!')

# Export qtp_al4_built_spacejoin to qtp_al4_built_spacejoin.txt
def exportTable_4():
    
    # Save the attribute table of qtp_al4_built_spacejoin as a txt file
    # Input dataset: qtp_al4_built_spacejoin
    # Output file: qtp_al4_built_spacejoin.txt
    
    # Open the file channel in write mode
    txt = open(str(name) + '_al4_built_spacejoin.txt', 'w')
    # Write the file header
    txt.write('AL4ID' + ',' + 'BUILT_AREA' + ',' + 'AL4_AREA' + ',' + 'AL4_RK' + '\n')
    # Read all rows of qtp_al4_built_spacejoin into 'rows'
    rows = arcpy.SearchCursor(str(name) + '_al4_built_spacejoin', fields='AL4_CODE;BUILT_AREA;AL4_AREA;pop2020')
    # Write all 'rows' into a text file named qtp_al4_built_spacejoin.txt
    for row in rows:
        context = str(row.getValue('AL4_CODE')) + ',' + str(row.getValue('BUILT_AREA')) + ',' + str(row.getValue('AL4_AREA')) + ',' + str(row.getValue('pop2020')) + '\n'
        txt.write(context)
    print('Spatial join file created!!!')

# Execute functions
def execute():

    # Record the start time of program execution
    start_time = time.time()
    addField_Calcul_2()
    spacejoin_3()
    exportTable_4()
    print(time.time() - start_time)
    # Output the runtime of this module to qtp_process1.txt
    txt = open(str(name)+'_process1.txt', 'w')
    txt.write('The RunTime of Process1.py is ' + str(time.time() - start_time) + '\n')

# Main caller program
execute()