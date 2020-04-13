import smtplib, ssl
import getpass

port = 465  # For SSL
sender_email = "rhNetMessenger@gmail.com"
receiver_email = "rhNetMessenger+receiver@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""


# Store Password
try: 
    password = getpass.getpass()
except Exception as error: 
    print('ERROR', error) 
else: 
    print('Password saved.') 

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("rhNetMessenger@gmail.com", password)
    
    # TODO: Send email here
    server.sendmail(sender_email, receiver_email, message)
    