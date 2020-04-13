from fpdf import FPDF
import datetime
import argparse

def generate_report(df, output_pdf_path):
    """
    A script that takes a dataframe and outputs the relevant data as a pdf
    """

    pdf = FPDF("P","mm","A4")
    pdf.add_page()
    def page_header():
        pdf.set_font('Arial',style='B', size=16)
        pdf.cell(0, 10, 'Vesuvius Alpha', 1,1)
        pdf.set_font('Arial',style='', size=10)
        pdf.cell(0, 8, 'A python project by Roberto Henríquez Perozo.',0,1)
        pdf.cell(0, 8, 'Data Analytics Bootcamp - IronHack Madrid.',0,1)
    
    # Generate landing page
    page_header()
    pdf.cell(0, 8, f'This report was generated on: {datetime.datetime.today()}',0,1)

    #pdf.cell(0, 8, f'Requested date(YYYY-MM): {args.year}{args.month}',0,1)


    def new_event_page(pandas_row):
        """
        This function will be once called for each existing event, to generate a correctly formatted response
        """
        pdf.add_page()
        page_header()
        pass
    
    """
    for i in range(len(df)):
        for e in df:
            pdf.cell(0,10,f'Volcano name: {df.iloc[i]}',0,1)
            #print(df.iloc[i])
    """

    pdf.output(output_pdf_path, 'F')
