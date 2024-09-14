import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class RouterScraper:
    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        chrome_options.add_argument('--no-sandbox')  # Required for running in some environments
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

        # Initialize the WebDriver with the specified options
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        """Login to the router using credentials from the .env file."""
        # Open the router login page
        router_url = os.getenv('ROUTER_URL')
        self.driver.get(router_url)
        time.sleep(12)  # Wait for the page to load

        # Find username and password fields and log in
        username = self.driver.find_element(By.NAME, 'username')
        password = self.driver.find_element(By.NAME, 'password')
        username.send_keys(os.getenv('APP_USERNAME'))
        password.send_keys(os.getenv('APP_PASSWORD'))
        password.send_keys(Keys.RETURN)
        time.sleep(7)  # Wait for the login process to complete

    def navigate_to_devices_page(self):
        """Navigate to the connected devices page."""
        devices_url = os.getenv('ROUTER_URL') + '/index.html#/gui/wifi/devices'
        self.driver.get(devices_url)
        time.sleep(20)

    def download_table(self):
        retries = 12  # Number of retries before giving up
        delay = 5    # Delay between retries in seconds

        for attempt in range(retries):
            try:
                # Locate the table wrapper by class name
                table_wrapper = self.driver.find_element(By.CLASS_NAME, 'uxfwk-table-wrapper')

                # Find the <tbody> element under the div
                tbody = table_wrapper.find_element(By.TAG_NAME, 'tbody')

                # Get the full HTML content of the <tbody>
                tbody_html = tbody.get_attribute('outerHTML')

                # Save the content to a file
                with open('live_table.html', 'w', encoding='utf-8') as file:
                    file.write(tbody_html)

                # print("Full <tbody> downloaded and saved to 'live_table.html'")
                return True  # Exit the function if successful

            except NoSuchElementException:
                print(f"\nTable or tbody not found. Attempt {attempt + 1} of {retries}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying

        print("\nFailed to download table after several attempts.")
        return False

    def close_driver(self):
        """Close the WebDriver."""
        self.driver.quit()

    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()

    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
