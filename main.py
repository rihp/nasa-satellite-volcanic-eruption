import argparse
import pandas as pd
from modules.vesuvius import *
from modules.cleaner import dataCleaner
from modules.presenter import generate_report
import modules.messenger as messenger

# 00 - WELCOME MESSAGE
say_hi()

# 01(a) - INPUT Paths
raw_dataset_path = 'INPUT/volcanic_dataset.xls' # RAW Data Source: SMITHSONIAN INSTITUTE or https://www.kaggle.com/martincontreras/volcanic-eruptions-dataset-all-to-2020
cached_data_csv_path = 'OUTPUT/enriched-data-cache.csv'
report_cache_csv_path = 'OUTPUT/report-cache.csv'
# 01(B) - OUTPUT Paths
output_csv_path = 'OUTPUT/enriched-data.csv'
pdf_output_path = 'OUTPUT/generated-pdf.pdf'
# Image outputs can be configured here

def parserFunction():
    # 02 - INSTRUCTIONS AND ARGUMENTS
    parser = argparse.ArgumentParser(description="Vesuvius is a retriever of satellite images. It currently uses a dataset containing volcanic eruptions and matches it with available photos from NASA's DSCOVR satellite, using the 'EPIC' API. The functionality of vesuvius has been desinged to be a modular program, in the sense that one could input a different dataset with relevant dates, and get the available satellite images from that date; Note that the DSCOVR satellite was launched into space on 2015, so older data will not be available. Also, very recent dates may not be available in the API's archive. DISCLAIMER: Use at your own risk.")
    parser.add_argument('year', help="This will be the year to filter. The correct input format: YYYY")
    parser.add_argument('month', help="This will be the month to filter. The correct input format: MM")
    parser.add_argument('--update', help="Functionality under development; When this flag is called, it should re-load the raw data, clean it, wrangle it, and then enrich it with the API data. The generated dataframe which includes the updated data will be saved at the `output_csv_path`, as well as in the `cached_data_csv_path` after running the program successfully.",
                                    action='store_true')
    parser.add_argument('--mailto', help="sends an email to the specified email.")
    #parser.add_argument('--version', help="displays vesuvius' version", )

    # 03 -PARSE ARGS AND CATCH ERRORS, like wrong lengths or formats
    args = parser.parse_args()
    if len(args.year) != 4:
        raise ValueError('The year has a wrong format. Try again using YYYY')
    if (len(args.month) != 2): # | (int(args.month) > 12)):
        raise ValueError('The year has a wrong format. Try again using MM')

    return args

def main(args):
       # 04 - LOAD DATA AND UPDATE
    if args.update == False:
        print(f' ~ Loading Cached Data from path: {cached_data_csv_path}')
        df = pd.read_csv(cached_data_csv_path)
    else:
        
        if updateData().upper() == 'CONTINUE':
            print(f' ~ updating data...\n ~ Loading RAW Data from path: {cached_data_csv_path}')
            # Run data cleaner
            df = pd.read_excel(raw_dataset_path, header=1)
            df = dataCleaner(df)
            # Enrich the `df` with API Data by calling the function which stores the data in new columns
            print(' ~ About to fetch from API, using the `enrich_from_api(df)` call')
            df = enrich_from_api(df)
        else:
            print(f' ~ Loading Cached Data from path: {cached_data_csv_path}')
            df = pd.read_csv(cached_data_csv_path)
    
    # 05 - FILTER available data with arguments
    print(f'Analyzing date YYYY-MM: {str(args.year)}-{str(args.month)}')
    df_filtered = df[(df.start_y == int(args.year)) & (df.start_m == int(args.month))]
    #df_filtered = df_filtered.drop(columns='Unnamed: 0') # I don't know why, an `Unnamed: 0` column is added automatically. 

    print(df_filtered) # ♠ OPTIMIZATION: SHOW AN ERROR MESSAGE WHEN THERE ARE NO REGISTERED EVENTS FOR THE SPECIFIED DATES

    # 06 - SUMMARY
    print(' ~ Summary of the data:\n ', df_filtered.describe())
    summary_df = df_filtered.describe()

    # 07 - EXPORT 
    print(" ~ Saving enriched data and caching report at 'OUTPUT' folder")
    df.to_csv(output_csv_path)
    df_filtered.to_csv(report_cache_csv_path)

    # 08 - FPDF
    print(" ~ Generating pdf report at 'OUTPUT' folder")
    report_kwargs = {'requested_year':args.year, 'requested_month':args.month}
    generate_report(df_filtered, pdf_output_path, report_kwargs)

    # 09 - EMAIL
    if args.mailto:
        messenger.send_attachment_email('senderemailshouldgohere', args.mailto ,'This is the `text_message` passed as an argument to the `send_text_email()` function called from main.py',
            pdf_output_path)

if __name__ == "__main__":
    args = parserFunction()
    main(args)
    pass