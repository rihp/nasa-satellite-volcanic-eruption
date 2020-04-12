import datetime

# The functions of the project will be stored in this file
def say_hi():
    print(f"""
    -----------------------
      Welcome to Vesuvius 
       Version Alpha 001 
    -----------------------
    Today is {datetime.date.today()}""")

def getSat():
    pass

def enrich_from_api():
    pass

def updateData():
    user_confirmation = input("""WAIT A SECOND! ARE YOU SURE THAT YOU WANT TO UPDATE THE DATA?
       
       THIS PROCESS WILL TAKE SOME TIME, AND IS *NOT RECOMMENDED*
       UNLESS YOU KNOW WHAT YOU ARE DOING. YOU RISK LOSING THE 
       CACHED DATA AND BEAKING THE REPORT FUNCTUIONALITIES.
       
       To proceed with the update, type 'CONTINUE UPDATE'. Else,
       if you want to skip the update, type 'NO'.""")

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

def report():
    pass

def export_data():
    pass