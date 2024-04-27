# qtp represents "Qinghai-Tibet Plateau"
# sp represents "sample"
# strtf represents "stratified"
# ssp represents "stratified sampling"
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
# thspop represents "Tibetan Human Settlement population grid, THS-POP"

import pandas as pd

def sample_info(sample_path, save_path, strtf_path):
    '''
    # Calculate basic information of samples
    :param sample_path: Top-level path where training samples are stored
    :param save_path: Top-level path where sample basic information is stored
    :param strtf_path: Path to CSV files containing zone sample data
    :return: None
    '''
    n = 0
    covariate_list = ['DEM', 'LR', 'SLP', 'AMP', 'AMT', 'NDVI', 'DTR', 'SKD', 'DTS', 'TA', 'THSPOP']
    # Get sample file names
    name_list = ['sample_' + str(i) for i in range(1, 51)]
    # Build header for basic information dataframe
    df = pd.DataFrame(columns=['Attribute', 'Minimum', 'Maximum', 'Mean', 'Standard Deviation'])
    # Read zone sample data
    data = pd.read_csv(strtf_path)
    # Calculate basic information for 10 covariates in the zone
    for idx, covariate in zip(range(1, 12), covariate_list):
        df.loc[idx] = [covariate, round(data[covariate].min(), 2), round(data[covariate].max(), 2), round(data[covariate].mean(), 2), round(data[covariate].std(), 2)]
    # Add an empty row
    df.loc[12] = ['', '', '', '', '']
    # Loop through training samples
    for name in name_list:
        n += 13
        i = 0
        data = pd.read_csv(sample_path + '\\' + name + '.csv')
        for idx, covariate in zip(range(n, n+12), covariate_list):
            i += 1
            df.loc[idx] = [covariate, round(data[covariate].min(), 2), round(data[covariate].max(), 2), round(data[covariate].mean(), 2), round(data[covariate].std(), 2)]
        # Add an empty row after calculating basic information for each training sample
        df.loc[n+i] = ['', '', '', '', '']
    df.to_csv(save_path + '\\' + 'Sample_Quality_Assessment.csv', index=False, encoding='utf-8')

def execute():
    # Folder names where training samples are stored
    sp_list = ['spR01', 'spR02', 'spR03', 'spR04', 'spR05', 'spR06', 'spR07', 'spR08', 'spR09', 'spR10', 'spR11', 'spR12', 'spR13', 'spR14', 'spR15', 'spR16']
    # Iterate through two groups
    for group in ['1', '2']:
        for sp in sp_list:
            # Path to training sample data
            sample_path = 'D:\\QTP\\RF\\03final\\RF_5000\\03SP\\02sample_data\\' + group + '\\' + sp
            # Path to save sample basic information
            save_path = 'D:\\QTP\\RF\\03final\\RF_5000\\03SP\\03sample_evaluate\\' + group + '\\' + sp
            # Path to zone sample data
            strtf_path = 'D:\\QTP\\RF\\03final\\RF_5000\\03SP\\03sample_evaluate\\strtf_sample\\' + sp + '\\' + sp + '.csv'
            sample_info(sample_path, save_path, strtf_path)

# Main function
execute()