from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
import pygetwindow as gw


# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Navigate to Spotify login
    driver.get("https://accounts.spotify.com/en/login")

    # Wait for the username field and enter the email
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-username")))
    username_field.send_keys('@gmail.com') #Enter your spotify email adres here

    # Wait for the password field and enter the password
    password_field = driver.find_element(By.ID, "login-password")
    password_field.send_keys('') #Enter your spotify password here

    # Add some delay to see what happens on the screen
    time.sleep(2)

    # Using JavaScript click to avoid potential issues with element reloads
    login_button = driver.find_element(By.ID, "login-button")
    driver.execute_script("arguments[0].click();", login_button)

    # Wait for login to complete and redirect to the user's account page
    time.sleep(2)

    # Navigate to order history
    driver.get("https://spotify.com/be-nl/account/order-history/")

    # Wait for the order history page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table")))

    # Find the first "Meer details" link for the latest invoice and click it
    latest_invoice_link = driver.find_element(By.XPATH, "(//a[contains(text(), 'Meer details')])[1]")
    latest_invoice_link.click()
    
    time.sleep(2)
    
    # Simulate Ctrl+P to open the print dialog (if not already opened)
    pyautogui.hotkey('ctrl', 'p')

    # Wait for the print dialog to appear
    time.sleep(2)
    pyautogui.press('enter')  # Select Save as PDF
    time.sleep(2)
    # Ensure the Save Print Output As window is focused and type the filename
    save_window = None
    for window in gw.getWindowsWithTitle('Save Print Output As'):
        if window.isActive:
            save_window = window
            break
    
    if save_window:
        save_window.activate()
        time.sleep(1)  # Give some time for the window to be active

        # Type the file name and save
        pyautogui.typewrite('latest_invoice.pdf')
        time.sleep(1)  # Optional: wait a bit before pressing Enter

        pyautogui.press('enter')

        time.sleep(2)

        print("Invoice downloaded successfully.")
    else:
        print("Save Print Output As window not found.")


finally:
    driver.quit()




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
email_to = "vendor-bills@gijsfintraxio.odoo.com"  # Replace with recipient's email address
email_subject = "Latest Invoice"

# SMTP server configuration (Gmail example)
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = "ucllqueue@gmail.com"  # Replace with your Gmail address
smtp_password = ""  # Replace with your Gmail password

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