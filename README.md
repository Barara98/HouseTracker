# HouseTracker 
Purpose:
This project tracks if all household members are home by checking which devices are connected to the home Wi-Fi.

## How It Works:
Router Scraping: Logs into the router to fetch connected devices.

Data Matching: Compares the connected devices with a list of known MAC addresses to identify who's home.

Automation & Manual Trigger: The system runs automatically every 60 seconds, but can be manually triggered for real-time data.

## Technologies Used:
Python

Selenium: For scraping the router’s web interface.

Pandas: For data processing.

BeautifulSoup: For HTML parsing.

Threading: For handling manual data fetching alongside automated checks.

## Setup:
### 1.Find Your Router's Web Interface:
Every router is different, so you’ll need to look up how to access the admin interface and scrape connected device data for your specific router model. You can usually access the router’s interface through a browser by visiting http://192.168.x.x.

### 2.Environment Variables:
Change the templateENV to .env file and fill your own information.

### 3.Install dependencies:
pip install -r requirements.txt
### 4.Run the system:
python main.py

Press 'm' during execution for manual fetching.

**Stay updated on who's home!**
