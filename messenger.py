import smtplib, ssl
import getpass

def send_text_email(sender_email, receiver_email, text_message):
    port = 465  # For SSL
    sender_email = "rhNetMessenger@gmail.com"
    receiver_email = receiver_email
    message = f"""\
    Subject: Hi there

    This message is sent from Vesuvius automatic messenger system:
    
    -----------

    {text_message}"""


    # Store Password
    try: 
        password = getpass.getpass('Messenger access code:')
    except Exception as error: 
        print('ERROR', error) 
    else: 
        print('Access code received.') 

    # Create a secure SSL context
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print(' ~ Logging in')    
        server.login("rhNetMessenger@gmail.com", password)
        
        # Send email here
        print(' ~ Sending message')
        server.sendmail(sender_email, receiver_email, message)

        print(' ~ They image should have been sent, check the inbox.')
        