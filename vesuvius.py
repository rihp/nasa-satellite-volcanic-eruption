# The functions of the project will be stored in this file
import datetime
import requests

def say_hi():
    print(f"""
    -----------------------
      Welcome to Vesuvius 
       Version Alpha 001 
    -----------------------
      Today is {datetime.date.today()}
    
    """)

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
    date = f"{YYYY}-{MM}-{DD}"
    
    # Define types of image collections and size to retrieve
    collections = {'nat': 'natural', 'enh':'enhanced'}

    size = {'png': ['png', 'png'],
            'jpg': ['jpg', 'jpg'],
            'thumb': ['thumbs', 'jpg']}
    
    # Request API metadata using input arguments defined during the call of the function, as well as the query parameters
    host = f'https://epic.gsfc.nasa.gov'
    metadata = f"{host}/api/{collections[collection]}/date/{date}"
    res = requests.get(metadata, params=queryParams)
    
    # Store relevant data from requests' response body as a `data` list type
    data = []
    for e in res.json():
        data.append((e['image'], e['centroid_coordinates'], e['date']))
    
    # Report status of requests' query response
    print(res.status_code, res.url)
    print(f"There are {len(res.json())} satellite images available for this date: {date}")
    
    # Parting from the recently-stored `data` variable store the following information:
    # 1. Construct and store the img-resource url
    # 2. Store the Centroid coordinates
    # 3. Store the available images in the response.json()
    ## All of this is stored in a `satellite_images` list type
    ### ♠ OPTIMIZATION: Apparently, this function returns a complete list of the available images for that specific requested day.
    ### This data can be leveraged in future versions of vesuvius
    satellite_images = []
    if len(data) > 0:
        for e in data:
            img = f"{host}/archive/{collections[collection]}/{YYYY}/{MM}/{DD}/{size[img_type][0]}/{e[0]}.{size[img_type][1]}"
            satellite_images.append([img, e[1], len(res.json())])
            
    #Return relevant data as list
    return satellite_images


def enrich_from_api(df):
    """Version '01'
    Depends on the getSat() function.
    For each event in the dataset, uses the getSat() function to retrieve the first available image datapoint

    It may need to recive INPUT:
     - the `df` variable

    OUTPUT:
    A list of lists, containing the `data` fetched for each requested event
    After calling the function and asiging the returned data to a variable, the data should be immediately assigned to the new corresponding columns of the input `df`

    """
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
    for phase_start in df['start']:
        print()
        print(phase_start)
        
        # Make the request to the API and store the data for a moment
        ## Normally, the output from this request should include several image urls
        ## at the next step of this function I pick only the last element.
        phase_data = getSat('nat', 'thumb', *phase_start.split('-'))
        
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
    user_confirmation = input("""WAIT A SECOND! ARE YOU SURE THAT YOU WANT TO UPDATE THE DATA?
       
       THIS PROCESS WILL TAKE SOME TIME, AND IS *NOT RECOMMENDED*
       UNLESS YOU KNOW WHAT YOU ARE DOING. YOU RISK LOSING THE 
       CACHED DATA AND BEAKING THE REPORT FEATURES OF VESUIVIUS.
       
       To proceed with the update, type 'CONTINUE UPDATE'.
       Else, if you want to skip the update, type 'NO'.""")

    if user_confirmation == 'CONTINUE UPDATE':
        print("""
        This will take a while. Making one request for each registered volcanic eruptive phase""")
        #Turn on verbose

        #Call the data cleaner
        
        #Specity which type of images the user wants to retrieve
        # enhanced, natural
        # png, jpg, thumb
        
        #Call the API data retriever

        #Turn off verbose
    else: 
        print(' ~ Update canceled.')
def report():
    pass

def export_data():
    pass