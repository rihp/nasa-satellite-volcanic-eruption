# The functions of the project will be stored in this file
import datetime
import requests
import pandas as pd
from verbositymod import *


def say_hi():
    print(f"""
    -----------------------
      Welcome to Vesuvius 
       Version Alpha 001 
    -----------------------
      Today is {datetime.date.today()}
    
    """)

def timestamp_to_str(TimeStamp):
    """
    turns a pandas.tslib.Timestamp into a 'YYYY-MM-DD' string
    """
    print('Input: TimeStamp', TimeStamp)
    """moment_in_time = {'year':TimeStamp.value.year, 
                'month':TimeStamp.value.month,
                'day':TimeStamp.value.day]
    }"""
    print(TimeStamp.year, TimeStamp.month)
    moment_in_time = [str(TimeStamp.year), str(TimeStamp.month), str(TimeStamp.day)]
    #print(moment_in_time)
    #print('processing Timestamp now')
    # Add 0 at the begining of `MM` if MM between 01 and 09
    if len(moment_in_time[1]) == 1:
        moment_in_time[1] = '0'+str(moment_in_time[1])
    
    # Add 0 at the begining of `DD` if DD between 01 and 09
    if len(moment_in_time[2]) == 1:
        moment_in_time[2] = '0'+str(moment_in_time[2])

    formatted_time = '-'.join(moment_in_time)
    
    return formatted_time


def getSat(collection, img_type, YYYY,MM,DD, queryParams=dict()):
    """Version 05.
     This function uses the `requests` module to GET the API data from NASA's DSCOVER Satellite archived image data.

     Input:
        The image collection to request (natural or enhanced images)
        The img_type (full-size .png, mid-size .jpg, or thumbnail .jpg)
        The date arguments (YYYY, DD, MM)

    Output:
        It returns the relevant pieces of the respose.json()
        Specifically, returns: 
            The first-available img-url
            The satellite coordinates for that image
                lat
                lon
            The ammount of images available for that specific day
            ♠ Optimization Idea: Time sensitivity can be assured with knowledge of UTC time and datetime modules
    """
    
    date = f"{str(YYYY)}-{str(MM)}-{str(DD)}"
    print(f'Trying to GET satellite data for this date: {date}')

    # Define types of image collections and possible sizes to retrieve from API
    collections = {'nat': 'natural', 'enh':'enhanced'}
    size = {'png': {'prefix':'png',
                    'sufix':'png'},
            'jpg': {'prefix':'jpg',
                    'sufix':'jpg'},
            'thumb': {'prefix':'thumbs',
                    'sufix':'jpg'}}
    
    # Request API metadata using input arguments defined during the call of the function, as well as the query parameters
    host = f'https://epic.gsfc.nasa.gov'
    metadata = f"{host}/api/{collections[collection]}/date/{date}"
    print(metadata)
    res = requests.get(metadata, params=queryParams)
    
    # Store relevant data from requests' response body as a `data` list type
    data = []
    for e in res.json():
        data.append((e['image'], e['centroid_coordinates'], e['date']))
    
    # Report status of requests' query response
    print(res.status_code, res.url)
    print(f"There are {len(res.json())} satellite images available for this date: {date}")
    
    # Parting from the recently-stored `data` variable store the following information:
    #   1. Construct and store the img-resource url
    #   2. Store the Centroid coordinates
    #   3. Store the available images in the response.json()
    #
    ## All of this is stored in a `satellite_images` list type
    ### ♠ OPTIMIZATION: Apparently, this function returns a complete list of the available images for that specific requested day.
    ### This data can be leveraged in future versions of vesuvius
    satellite_images = []
    if len(data) > 0:
        for e in data:
            # here the image url is constructed using available vars
            img = f"{host}/archive/{collections[collection]}/{YYYY}/{MM}/{DD}/{size[img_type]['prefix']}/{e[0]}.{size[img_type]['sufix']}"
            satellite_images.append([img, e[1], len(res.json())])
            
    #Return relevant data as list
    return satellite_images
    # I dont know why this was here. probably deprecated line.
    # return [img_urls, sat_lats, sat_lons, pics_that_day]

def enrich_from_api(df):
    """Version '01'
    Depends on the getSat() function.
    For each event in the dataset, uses the getSat() function to retrieve the first available image datapoint

    It may need to recive INPUT:
     - the `df` variable

    OUTPUT:
     - A list of lists, containing the `data` fetched for each requested event
     - After calling the function and asiging the returned data to a variable, the data should be immediately assigned to the new corresponding columns of the input `df`

    """
    print('Data enricher turned on')

    # What are we going to retrieve from each request?
    img_urls = []
    sat_lats = []
    sat_lons = []
    pics_that_day = []
    
    # Start looping the dataframe's array of dates.
    # Each value in the array (YYYY-MM-DD) must be separated with a '-', as it will be later split() by it.
    ## ♠ OPTIMIZATION IDEA: 
    ##   Check if the row in question has the data already
    ##   If it has it, copy it and add it to the new list
    ##   If it does not have the data, request and add it.

    count = 0
    for phase_start in df['start']:
        """
         Make the request to the API and store the data for a moment
         Normally, the output from this request should include several image urls
         at the next step of this function I pick only the last element.
        """
        timestamp_to_str(phase_start)
        phase_start = timestamp_to_str(phase_start)
        phase_data = getSat('nat', 'thumb', *phase_start.split('-'))
        print(f"`phase_data`: {phase_data}")
        #phase_data = getSat('nat', 'thumb', phase_start.year, phase_start, phase_start.year)
        

        count +=1

        # If there is data in the response, include the response data to the lists 
        if len(phase_data) > 0:
            
            # Indexes here are [0] because I only want to get the first image of the day
            ## ♠ OPTIMIZATION IDEA: 
            ## Possibly change the index to [-1] to get the last picture from that day.
            ## This would bring us a higher chance of seeing the effects of the eruption.
            ## If the retreived image is the first one of the day, there is a lower probability of the image capturing an eruption event
            print('This is the first available image for that date')
            print(phase_data[0])
            img_urls.append(phase_data[0][0])
            sat_lats.append(phase_data[0][1]['lat'])
            sat_lons.append(phase_data[0][1]['lon'])
            pics_that_day.append(phase_data[0][2])
            
        # If there are no images to retrieve, set append null values to the index
        else:
            img_urls.append('no-img')
            sat_lats.append('0')
            sat_lons.append('0')
            pics_that_day.append(0)
            
    # ♠ OPTIMIZATION IDEA: POSSIBLY INCLUDE A ZIP HERE ~
    
    return [img_urls, sat_lats, sat_lons, pics_that_day]

def updateData():
    user_confirmation = input("""
    
        WAIT A SECOND! ARE YOU SURE THAT YOU WANT TO UPDATE THE DATA?
       
        THIS PROCESS WILL TAKE SOME TIME, AND IS *NOT RECOMMENDED*
        UNLESS YOU KNOW WHAT YOU ARE DOING. YOU RISK LOSING THE 
        CACHED DATA AND BEAKING THE REPORT FEATURES OF VESUVIUS.
       
        To proceed with the update, type 'CONTINUE'.
        Else, if you want to skip the update, type 'NO'.
        
        """)

    if user_confirmation.upper() == 'CONTINUE':
        print("This will take a while. Making one request for each registered volcanic eruptive phase")
        # ♠♠ Turn on verbose
        
        #Call the data cleaner
        
        #Specity which type of images the user wants to retrieve
        # enhanced, natural
        # png, jpg, thumb
        
        #Call the API data retriever

        #Turn off verbose
        return user_confirmation.upper()
    else: 
        print(' ~ Update canceled.')
        return user_confirmation.upper()

def loadCacheData(cached_data_csv_path):
    """
    FUNCTION NOT IN USE AS OF 2020-04-13
    
    Takes the `cached_data_csv_path` and loads it in the right format for use in the vesuvius data pipeline
    When the function is called, it will `return` the loaded data, so one must assign it to a variable immediately.

    The idea is to use this returned data as values which can be assigned to new columns of the input `df`.

    INPUT: 
     - `cached_data_csv_path
    OUTPUT:
     - A list of lists, containing the `data` fetched for each requested event
        [img_urls, sat_lats, sat_lons, pics_that_day]
    """
    cached_df = pd.read_csv(cached_data_csv_path)
    #img_urls = cached_df['start_img']
    #sat_lats = cached_df['sat_lats']
    #sat_lons = cached_df['sat_lons']
    #pics_that_day = ['start_img_available_in_api']
    
    return df

def data_report(df):
    """
    takes a pandas `df`, prints it's description and returns it in the end
    """
    print(' ~ Summary of the data:\n ', df.describe())
    summary_df = df.describe()
    return summary_df

def export_data():
    pass