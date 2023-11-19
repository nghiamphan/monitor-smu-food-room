import smtplib
import time
import streamlit as st
import platform

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def is_registration_open():
    URL = st.secrets["URL"]

    if platform.processor() != "":
        driver_version = None
    else:
        driver_version = st.secrets["CHROME_DRIVER_VERSION"]
    service = Service(ChromeDriverManager(driver_version).install())

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(service=service, options=options)

    driver = get_driver()
    driver.get(URL)

    # wait for the entire web to be fetched
    time.sleep(0.1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for date in soup.select("div[class*='date circle']"):
        print(date["class"])
        if "not-bookable" not in date["class"]:
            return True

    return False


def send_email(receiver_email: str = None):
    # Email configuration
    SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
    SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]
    RECEIVER_EMAIL = receiver_email or st.secrets["RECEIVER_EMAIL"]
    EMAIL_SUBJECT = st.secrets["EMAIL_SUBJECT"]
    EMAIL_BODY = f"{st.secrets['EMAIL_BODY']}\n{st.secrets['URL']}"

    # Set up the MIME
    message = MIMEMultipart()
    message["Subject"] = EMAIL_SUBJECT

    # Attach the body to the email
    message.attach(MIMEText(EMAIL_BODY, "plain"))

    # Connect to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Start the TLS encryption
        server.starttls()

        # Log in to the Gmail account
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

    print("Email sent successfully.")


if __name__ == "__main__":
    print(is_registration_open())
    send_email()
