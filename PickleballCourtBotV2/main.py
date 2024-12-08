import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Configuration
USERNAME = ''
PASSWORD = ''
COURT_DATE = 'MM/DD/YYYY'  # Desired booking date
TIME_SLOT = 'desired_time'  # Time slot string visible on the site

# Function to run the script
def book_appointment():
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Use the appropriate WebDriver for your browser

    try:
        # Open the website
        driver.get('')

        # Wait for the login page to load and find login elements
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'loginname')))

        # Login
        username_field = driver.find_element(By.NAME, 'loginname')
        password_field = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//*[@id="wrapper"]/table[3]/tbody/tr/td/table/tbody/tr[2]/td[2]/form/table/tbody/tr[6]/td/input')  # Update with the actual button ID

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        login_button.click()

        # Wait for the booking page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "e_id")))

        #################################### Select Court ##########################################
        dropdown1 = driver.find_element(By.XPATH, "//*[@id='table-left']/tbody/tr[2]/td/table/tbody/tr[1]/td/select")
        select = Select(dropdown1)
        select.select_by_value("4807")  # Select pickle 1 (4807)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "service_id")))

        #################################### Select Play Time ##########################################
        dropdown2 = driver.find_element(By.NAME, "service_id")
        select = Select(dropdown2)
        select.select_by_value("6453")

        ################################## CALENDAR #####################################
        target_date = "20241210"  # Replace with the desired date in the same format

        date_xpath = f"//a[contains(@href, \"dosubmit('{target_date}',\")]"
        date_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, date_xpath))
        )
        date_element.click()

        ################################## Next Page #####################################
        next_page_button_xpath = "//*[@id='wrapper']/table[5]/tbody/tr/td[3]/div[1]/div/form/input[50]"
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_page_button_xpath))
        )
        next_page_button.click()

        ################################## Booking #####################################
        xpath_query = "//tr[td/div[contains(text(), 'Tuesday') and contains(text(), 'December 10, 2024')] and td/span[contains(text(), '7:00pm')] and td[contains(text(), 'Lexington Colony Pickleball Court 1')]]//input[@value='Book it']"

        book_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_query))
        )
        if book_button:
            book_button.click()
            print("Booking button clicked!")
        else:
            print("No matching 'Book it' button found.")

        ################################## Finalize Appointment #####################################
        finalize_appointment_button_xpath = "//*[@id='myForm2']/table[2]/tbody/tr/td/table/tbody/tr[4]/td/input[2]"
        finalize_appointment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, finalize_appointment_button_xpath))
        )
        finalize_appointment_button.click()

    finally:
        # Close the browser after booking
        driver.quit()

# Schedule the booking script to run at 12:00 AM
schedule.every().day.at("00:00").do(book_appointment)

print("Scheduler running. Waiting for midnight...")

# Keep the script running to allow scheduling
while True:
    schedule.run_pending()
    time.sleep(1)
