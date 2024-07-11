import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import os
from pathlib import Path

# Get the user's home directory
home = str(Path.home())

# Construct the path to the Downloads folder
downloads_folder = os.path.join(home, 'Downloads')

# Example usage:
file_name = 'latest_invoice.pdf'
file_path = os.path.join(downloads_folder, file_name)
# Email configuration
email_from = "ucllqueue@gmail.com"  # Replace with your email address
email_to = "ucllqueue@gmail.com"  # Replace with recipient's email address
email_subject = "Latest Invoice"

# SMTP server configuration (Gmail example)
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = "ucllqueue@gmail.com"  # Replace with your Gmail address
smtp_password = "ewvbbohcpgmvjupe"  # Replace with your Gmail password

# File path to the latest invoice PDF

# Create a multipart message
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = email_subject

# Attach the invoice PDF
with open(file_path, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename=latest_invoice.pdf')
    msg.attach(part)

# Connect to SMTP server and send email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {str(e)}")
finally:
    server.quit()

os.remove(file_path)