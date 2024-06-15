from email.message import EmailMessage  # Import EmailMessage class for creating email messages
import ssl  # Import ssl module for creating a secure SSL context
import smtplib  # Import smtplib for sending email using the Simple Mail Transfer Protocol (SMTP)

from utils import configReader


def sendmail(subject, body):
    print(subject)
    print(body)
    # Define the sender's email address and password
    email_sender = configReader.get_email_config('EMAIL')['email.sender']
    email_password = configReader.get_email_config('EMAIL')[
        'email.password']  # Password or app-specific password for the sender's email account

    # Define the receiver's email address
    email_receiver = configReader.get_email_config('EMAIL')['email.receiver']

    # Create an instance of EmailMessage
    em = EmailMessage()

    # Set the email headers: From, To, and Subject
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    # Set the email content/body
    em.set_content(body)

    # Create a secure SSL context for encrypted communication
    context = ssl.create_default_context()

    # Connect to the Gmail SMTP server using SMTP_SSL for a secure connection
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        # Log in to the SMTP server using the sender's email credentials
        smtp.login(email_sender, email_password)

        # Send the email
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Example usage:
# sendmail('Test Subject', 'This is the body of the email')
