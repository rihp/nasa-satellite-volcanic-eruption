import os
import argparse
import requests
import pandas as pd

# datetime module will probably give some errors as it's not imported with the same name
import datetime
from IPython.display import Image
from vesuvius import *

say_hi()

# Describe program usage instructions
# args
# --version
#
# --year
#
# --month
#
# --update='False'
#   will only reload the dataset and make the requests to the api when set to True
#   when False, vesuvius will look for the cached data from the last update.

# Data location INs and OUTs




# Run data cleaner



# Run the df filler with API Data




# Filter data with arguments
#df = pd.read_csv('OUTPUT/volcanic-explosions.csv')



# Print summary data
#df.describe


# Export to PDF


