import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the MIME
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Quit the server
    server.quit()

# Example usage:
sender_email = "xxxxxx@gmail.com"

# 16 digits google app password  
sender_password = "xxxxxxxxxxxxxxxx"
recipient_email = "aaaaaaa@gmail.com"

subject = "Test Email"
message = "This is a test email sent from Python."

send_email(sender_email, sender_password, recipient_email, subject, message)