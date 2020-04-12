import os
import argparse
import requests
import pandas as pd

# datetime module will probably give some errors as it's not imported with the same name
import datetime
from IPython.display import Image
from vesuvius import *

# Welcome Message
#say_hi()
print('hi!')

# Describe program usage instructions
parser = argparse.ArgumentParser()

# --version
parser.add_argument('--version', help="displays vesuvius' version")
# --year
parser.add_argument('year', help="This will be the year to filter", type=int)
# --month
#
# --update='False'
#   will only reload the dataset and make the requests to the api when set to True
#   when False, vesuvius will look for the cached data from the last update.
args = parser.parse_args()


# Data location INs and OUTs




# Run data cleaner



# Run the df filler with API Data




# Filter data with arguments
#df = pd.read_csv('OUTPUT/volcanic-explosions.csv')
print(f'Analyzing year {str(args.year)}')

# Print summary data
#df.describe


# Export to PDF


