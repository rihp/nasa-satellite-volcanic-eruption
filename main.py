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
print('hi, welcome to vesuvius alpha!')
########################################################################################################


# 01 - INSTRUCTIONS AND ARGUMENTS
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

# 02 -PARSE ARGS AND CATCH ERRORS
args = parser.parse_args()
if len(args.year) != 4:
    raise ValueError('The year has a wrong format. Try again using YYYY')
if len(args.month) != 2:
    raise ValueError('The year has a wrong format. Try again using MM')
########################################################################################################


# 03 - INPUTS AND OUTPUTS PATHS
#df = pd.read_csv('OUTPUT/volcanic-explosions.csv')
########################################################################################################

# 04 - UPDATE
## Run data cleaner
#
## Run the df filler with API Data
# 
########################################################################################################

# 05 - FILTER available data with arguments
print(f'Analyzing date YYYY-MM: {str(args.year)}-{str(args.month)}')
########################################################################################################

# 06 - SUMMARY
#df.describe
########################################################################################################

# 07 - EXPORT 
# FPDF


