import argparse
import pandas as pd
from vesuvius import *
from cleaner import dataCleaner

# 00 - WELCOME MESSAGE
say_hi()
########################################################################################################

# 01 - INPUT / OUTPUT PATHS
# INPUTS
## RAW Data Source: https://www.kaggle.com/martincontreras/volcanic-eruptions-dataset-all-to-2020
## OR SMITHSONIAN INSTITUTE
raw_dataset_path = 'INPUT/volcanic_dataset.xls' 
cached_data_csv_path = 'OUTPUT/enriched-data-cache.csv'
report_cache_csv_path = 'OUTPUT/report-cache.csv'
# OUTPUTS
output_csv_path = 'OUTPUT/enriched-data.csv'
# Image outputs can be configured here
########################################################################################################

# 02 - INSTRUCTIONS AND ARGUMENTS
parser = argparse.ArgumentParser(description="Vesuvius is a retriever of satellite images. It currently uses a dataset containing volcanic eruptions and matches it with available photos from NASA's DSCOVR satellite, using the 'EPIC' API. The functionality of vesuvius has been desinged to be a modular program, in the sense that one could input a different dataset with relevant dates, and get the available satellite images from that date; Note that the DSCOVR satellite was launched into space on 2015, so older data will not be available. Also, very recent dates may not be available in the API's archive. DISCLAIMER: Use at your own risk.")
parser.add_argument('year', help="This will be the year to filter. The correct input format: YYYY")
parser.add_argument('month', help="This will be the month to filter. The correct input format: MM")
parser.add_argument('--update', help="Functionality under development; When this flag is called, it should re-load the raw data, clean it, wrangle it, and then enrich it with the API data. The generated dataframe which includes the updated data will be saved at the `output_csv_path`, as well as in the `cached_data_csv_path` after running the program successfully.",
                                 action='store_true')
# parser.add_argument('--version', help="displays vesuvius' version")
########################################################################################################

# 03 -PARSE ARGS AND CATCH ERRORS
args = parser.parse_args()
# Raise errors related to wrong date formats
if len(args.year) != 4:
    raise ValueError('The year has a wrong format. Try again using YYYY')
if (len(args.month) != 2): # | (int(args.month) > 12)):
    raise ValueError('The year has a wrong format. Try again using MM')
########################################################################################################

# 04 - LOAD DATA AND UPDATE
if args.update == False:
    print(f' ~ Loading Cached Data from path: {cached_data_csv_path}')
    df = pd.read_csv(cached_data_csv_path)
    loaded_data_list = loadCacheData(cached_data_csv_path)
else:
    user_response = updateData()
    if user_response.upper() == 'CONTINUE':
        print(f' ~ updating data...\n ~ Loading RAW Data from path: {cached_data_csv_path}')
        ## Run data cleaner
        df = pd.read_excel(raw_dataset_path, header=1)
        df = dataCleaner(df)

        ## Enrich the `df` with API Data by calling the function and storing the data in new columns
        print(' ~ About to fetch from API, using the `enrich_from_api(df)` call')
        loaded_data_list = enrich_from_api(df)
        print(' ~ About to call the `updateData()` function')

        df['start_img'] = loaded_data_list[0]
        df['sat_lats'] = loaded_data_list[1]
        df['sat_lons'] = loaded_data_list[2]
        df['start_img_available_in_api'] = loaded_data_list[3]
    else:
        print(f' ~ Loading Cached Data from path: {cached_data_csv_path}')
        df = pd.read_csv(cached_data_csv_path)
        loaded_data_list = loadCacheData(cached_data_csv_path)        


# 05 - FILTER available data with arguments
print(f'Analyzing date YYYY-MM: {str(args.year)}-{str(args.month)}')
df_filtered = df[(df.start_y == int(args.year)) & (df.start_m == int(args.month))]

## I don't know why, an `Unnamed: 0` column is added automatically. 
#df_filtered = df_filtered.drop(columns='Unnamed: 0')

# ♠ OPTIMIZATION: SHOW AN ERROR MESSAGE WHEN THERE ARE NO REGISTERED EVENTS FOR THE SPECIFIED DATES
print(df_filtered, '\n')
print(f" ~ Resulting shape of the DataFrame:\n{df_filtered.shape} \n")
########################################################################################################

# 06 - SUMMARY
print(' ~ Summary of the data:\n ', df_filtered.describe())
summary_df = df_filtered.describe()
########################################################################################################

# 07 - EXPORT 
print(" ~ Saving enriched data and caching report at 'OUTPUT' folder")
df.to_csv(output_csv_path)
df_filtered.to_csv(report_cache_csv_path)

# FPDF
