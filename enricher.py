# Fills dataset with image urls
import requests
#import os
#from IPython.display import Image
import pandas as pd
#import numpy as np
#import datetime

df = pd.read_csv('OUTPUT/volcanic-eruptions.csv')

def getSat(collection, img_type, YYYY,MM,DD, queryParams=dict()):
    
    date = f"{YYYY}-{MM}-{DD}"
    
    # Define types of image collections and size 
    collections = {'nat': 'natural', 'enh':'enhanced'}

    size = {'png': ['png', 'png'],
            'jpg': ['jpg', 'jpg'],
            'thumb': ['thumbs', 'jpg']}
    
    
    # Request API metadata using query parameters
    host = f'https://epic.gsfc.nasa.gov'
    metadata = f"{host}/api/{collections[collection]}/date/{date}"
    res = requests.get(metadata, params=queryParams)
    
    
    # Store reelevant data from requests' response body
    data = []
    for e in res.json():
        data.append((e['image'], e['centroid_coordinates'], e['date']))
    
    
    # Report status of query response
    print(res.status_code, res.url)
    print(f"There are {len(res.json())} satellite images available for this date: {date}")

    
    # Construct the image resource url
    satellite_images = []
    if len(data) > 0:
        for e in data:
            img = f"{host}/archive/{collections[collection]}/{YYYY}/{MM}/{DD}/{size[img_type][0]}/{e[0]}.{size[img_type][1]}"
            satellite_images.append([img, e[1], len(res.json())])
            
    #Return relevant data as list
    return satellite_images

# Access the START dates on each eruptive phase

# Add arguments for which types of images i want to retrieve (natural/enhanced) (png, jpg, thumb)
def enrich_from_api():
# Version '01'

    # What are we going to retrieve from each request?
    img_urls = []
    sat_lats = []
    sat_lons = []
    pics_that_day = []
    
    # Start looping the dataframe
    ## ♠ OPTIMIZATION IDEA: 
    ##   Check if the row in question has the data already
    ##   If it has it, copy it and add it to the new list
    ##   If it does not have the data, request and add it.
    for phase_start in df['start']:
        print()
        print(phase_start)
        
        # Make the request to the API and store the data for a moment
        ## Normally, the output from this request should include several image urls
        ## at the next step of this function I pick only the last element
        phase_data = getSat('nat', 'thumb', *phase_start.split('-'))
        
        # If there is data in the response, include the response data to the lists 
        if len(phase_data) > 0:
            
            # Indexes here are [0] because I only want to get the first image of the day
            # Possibly change the index to [-1] to get the last picture from that day 
            print('This is the first available image for that date')
            print(phase_data[0])
            img_urls.append(phase_data[0][0])
            sat_lats.append(phase_data[0][1]['lat'])
            sat_lons.append(phase_data[0][1]['lon'])
            pics_that_day.append(phase_data[0][2])
            
        # If there are no images to retrieve, set the null values
        else:
            img_urls.append('no-img')
            sat_lats.append('0')
            sat_lons.append('0')
            pics_that_day.append(0)
            
            
    # POSSIBLY INCLUDE A ZIP HERE ~
    
    return [img_urls, sat_lats, sat_lons, pics_that_day]


# Watch out, this cell takes about 4 minutes to run
# ♠ OPTIMIZATION IDEA: 
## Define this as 'vesuvius.updateData()' to be called from main.py when `--update` flag is True

# Call the function
print('About to fetch from API')
new_data = enrich_from_api()

# Store the new data in the following columns
df['start_img'] = new_data[0]
df['sat_lats'] = new_data[1]
df['sat_lons'] = new_data[2]
df['start_img_available_in_api'] = new_data[3]

# OUTPUT: 
#     The dataframe with 4 new columns
#       start_img 	
#       sat_lats 	
#       sat_lons 	
#       start_img_available_in_api
print(" ~ Here's a sample of the enriched Data Frame:")
print(df[20:50])
df.to_csv('OUTPUT/enriched-data.csv')
