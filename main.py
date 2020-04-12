import argparse
#import requests
import pandas as pd
import datetime #datetime module will probably give some errors as it's not imported with the same name
#from IPython.display import Image
#import os
#import subprocess
from vesuvius import *
########################################################################################################

# 00 - WELCOME MESSAGE
#say_hi()
print('Hi,\n Welcome to Vesuvius Alpha!')
########################################################################################################


# 01 - INPUTS AND OUTPUTS PATHS
df = pd.read_csv('OUTPUT/volcanic-eruptions.csv') # maybe move this to Step 4, and only hold here the path to files
# raw_data_path = 'INPUT/here.csv'
# enriched_data_path = 'OUTPUT/there.csv'
# df = pd.read_csv('OUTPUT/volcanic-eruptions.csv')
########################################################################################################


# 02 - INSTRUCTIONS AND ARGUMENTS
parser = argparse.ArgumentParser(description="Vesuvius is a retriever of satellite images. It currently uses a dataset containing volcanic eruptions and matches it with available photos from NASA's DSCOVR satellite, using the 'EPIC' API. The functionality of vesuvius has been desinged to be a modular program, in the sense that one could input a different dataset with relevant dates, and get the available satellite images from that date; Note that the DSCOVR satellite was launched into space on 2015, so older data will not be available. Also, very recent dates may not be available in the API's archive. DISCLAIMER: Use at your own risk.")
## year
parser.add_argument('year', help="This will be the year to filter. The correct input format: YYYY")
## month
parser.add_argument('month', help="This will be the month to filter. The correct input format: MM")
## --version
parser.add_argument('--version', help="displays vesuvius' version")
## --update='False'
##   will only reload the dataset and make the requests to the api when set to True
##   when False, vesuvius will look for the cached data from the last update.
# parser.add_argument('--update', help="functionality under development, action='store_true'")
########################################################################################################

# 03 -PARSE ARGS AND CATCH ERRORS
args = parser.parse_args()
if len(args.year) != 4:
    raise ValueError('The year has a wrong format. Try again using YYYY')
if len(args.month) != 2:
    raise ValueError('The year has a wrong format. Try again using MM')
########################################################################################################
#print('STEP 03 DONE\n')

# 04 - UPDATE
## Run data cleaner
#bash_commad('python3 cleaner.py')
## Run the df filler with API Data
#bash_command('python3 enricher.py') 
########################################################################################################



# 05 - FILTER available data with arguments
print(f'Analyzing date YYYY-MM: {str(args.year)}-{str(args.month)}')
## 
#df_filtered = df[df.start_y == int(args.year)][df.start_m == int(args.month)]
df_filtered = df[(df.start_y == int(args.year)) & (df.start_m == int(args.month))]

## I don't know why, an `Unnamed: 0` column is added automatically. 
df_filtered = df_filtered.drop(columns='Unnamed: 0')

# ♠ OPTIMIZATION: SHOW AN ERROR MESSAGE WHEN THERE ARE NO REGISTERED EVENTS FOR THE SPECIFIED DATES
print(df_filtered, '\n')
print(f" ~ Resulting shape of the DataFrame:\n{df_filtered.shape} \n")
########################################################################################################





# 06 - SUMMARY
print(' ~ Summary of the data:\n ', df_filtered.describe())
########################################################################################################




# 07 - EXPORT 
# FPDF


