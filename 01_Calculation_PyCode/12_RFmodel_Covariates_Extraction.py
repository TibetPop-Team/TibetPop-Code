# _*_ coding:utf-8 _*_
# qtp represents "Qinghai-Tibet Plateau"
# rf represents "random forest"

# Import third-party libraries required for operations
import time
import arcpy
arcpy.env.overwriteOutput = True

# Create a decorator to calculate the execution time of a function
def print_execute_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        # Output the runtime of this module to a txt file
        txt = open('D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\py\\03CovariateExtraction.txt', 'w')
        txt.write('The RunTime of 03impactBymask.py is ' + str(end_time - start_time) + '\n')
        print('success!')
    return wrapper

def extractByMask(impact_path, mask_path, save_path):
    '''
    Extracts impact factor data based on the zoning mask.
    :param impact_path: Primary path where impact factor data is stored.
    :param mask_path: Primary path where mask data is stored.
    :param save_path: Path to save parameter information.
    :return: None
    '''
    # Acquire permission to use ArcGIS spatial module
    arcpy.CheckOutExtension('Spatial')
    arcpy.env.workspace = impact_path
    mask = mask_path
    ralist = arcpy.ListRasters()
    for item in ralist:
        # Skip population density label data
        if item == 'qtp_thspop.tif':
            continue
        # Extract impact factor data meeting the condition by mask
        outExtractByMask = arcpy.sa.ExtractByMask(item, mask)
        name = item.split('_')[1]
        outExtractByMask.save(save_path + '\\' + name)

@print_execute_time
def execute():
    '''
    Main function
    :param: None
    :return: None
    '''
    impact_path = 'D:\\QTP\\RF\\03final\\RF_5000\\01IMPACT_DATA'
    # Set the names of zoning masks
    mask_list = ['zoneR01', 'zoneR02', 'zoneR03', 'zoneR04', 'zoneR05', 'zoneR06', 'zoneR07', 'zoneR08', 'zoneR09', 'zoneR10', 'zoneR11', 'zoneR12', 'zoneR13', 'zoneR14', 'zoneR15', 'zoneR16']
    for group in ['1', '2']:
        for mask in mask_list:
            mask_path = 'D:\\QTP\\RF\\03final\\RF_5000\\02MASK\\' + mask + '.tif'
            save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\04PREDICT\\' + group + '\\' + mask + '\\02test'
            extractByMask(impact_path, mask_path, save_path)

# Main calling function
execute()