# Module created following this tutorial: https://realpython.com/python-send-email/
import email, smtplib, ssl
import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        print(' ~ Sending Simple Text message')
        server.sendmail(sender_email, receiver_email, message)

        print(' ~ They image should have been sent, check the inbox.')

def send_html_email(sender_email, receiver_email, text_message):
    """
    Today’s most common type of email is the MIME (Multipurpose
    Internet Mail Extensions) Multipart email, combining HTML
    and plain-text. MIME messages are handled by Python’s email.mime module. 
    
    For a detailed description, check the documentation.
    
    https://docs.python.org/3/library/email.mime.html
    """
    # Basic email config
    port = 465  # For SSL
    sender_email = "rhNetMessenger@gmail.com"
    receiver_email = receiver_email
    try: # Store Password
        password = getpass.getpass('Messenger access code:')
    except Exception as error: 
        print('ERROR', error) 
    else: 
        print('Access code received.') 

    # Format Message
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test subject"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text_message = f"""\
    Subject: Hi there
    This message is sent from Vesuvius automatic messenger system:
    -----------------
    {text_message}
    """

    html_formatter = f"""\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="https://github.com/rihp/nasa-satellite-volcanic-eruptions"> Check out my new project</a> 
        . You'll enjoy it quite a lot!
        </p>
        <p> This message is for you:<br>
        {text_message}
        </p>
    </body>
    </html>
    """
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text_message, "plain")
    part2 = MIMEText(html_formatter, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # (The email client will try to render the last part first)
    message.attach(part1)
    message.attach(part2)

    # Create a secure SSL context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print(' ~ Logging in')    
        server.login("rhNetMessenger@gmail.com", password)
        
        # Send email here
        print(' ~ Sending HTML + Text message')
        server.sendmail(
        sender_email, receiver_email, message.as_string()
        )
        print(' ~ They image should have been sent, check the inbox.')

def send_attachment_email(sender_email, receiver_email, text_message, attachment_path):
    """
    Today’s most common type of email is the MIME (Multipurpose
    Internet Mail Extensions) Multipart email, combining HTML
    and plain-text. MIME messages are handled by Python’s email.mime module. 
    
    For a detailed description, check the documentation.
    
    https://docs.python.org/3/library/email.mime.html
    """
    # Basic email config
    port = 465  # For SSL
    sender_email = "rhNetMessenger@gmail.com" 
    receiver_email = receiver_email
    try: # Store Password
        password = getpass.getpass('Messenger access code:')
    except Exception as error: 
        print('ERROR', error) 
    else: 
        print('Access code received.') 

    # Format Message
    message = MIMEMultipart("alternative")
    message["Subject"] = "attached files - test email subject"
    message["From"] = sender_email
    #message["To"] = receiver_email
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Create the plain-text version of your message
    text_message = f"""\
    Subject: Hi there
    This message is sent from Vesuvius automatic messenger system:
    -----------------
    {text_message}
    """

    # Create the HTML version of your message
    html_formatter = f"""\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="https://github.com/rihp/nasa-satellite-volcanic-eruptions"> Check out my new project</a> 
        . You'll enjoy it quite a lot!
        </p>
        <p> This message is for you:<br>
        {text_message}
        </p>
    </body>
    </html>
    """
    # Turn these into plain/html MIMEText objects
    part1_text = MIMEText(text_message, "plain")
    part2_html = MIMEText(html_formatter, "html")

    # PART 3 - Attaching a file:
    # Open PDF file in binary mode
    with open(attachment_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part3_attachment = MIMEBase("application", "octet-stream")
        part3_attachment.set_payload(attachment.read())


    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part3_attachment)

    # Add header as key/value pair to attachment part
    part3_attachment.add_header(
    "Content-Disposition",
    f"attachment; filename= {attachment_path}",
    )

    # Add Attachment, HTML and plain-text parts to MIMEMultipart message
    # (The email client will try to render the last part first)
    message.attach(part1_text)
    message.attach(part2_html)
    message.attach(part3_attachment)

    # Create a secure SSL context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print(' ~ Logging in')    
        server.login("rhNetMessenger@gmail.com", password)
        
        # Send email here
        print(' ~ Sending HTML + Text message')
        server.sendmail(
        sender_email, receiver_email, message.as_string()
        )
        print(' ~ They image should have been sent, check the inbox.')
    