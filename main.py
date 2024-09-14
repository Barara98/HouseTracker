import threading
import pandas as pd
from live_data import extract_table_data
from router import RouterScraper


class MonitoringSystem:
    def __init__(self):
        self.router = RouterScraper()
        self.manual_fetch_event = threading.Event()  # Event to signal manual fetch
        self.login = False

    def run(self):
        # Start thread for manual triggering
        manual_thread = threading.Thread(target=self.listen_for_manual_trigger, daemon=True)
        manual_thread.start()

        # Automated process loop
        while True:
            # Perform data fetch and processing
            self.fetch_and_process_data()

            # Wait for either manual fetch trigger or timeout
            self.manual_fetch_event.wait(timeout=60)

            # Clear the event for next cycle
            self.manual_fetch_event.clear()

    def login_and_navigate(self):
        if not self.login:
            self.router.login()
            self.router.navigate_to_devices_page()
            self.login = True

    def fetch_and_process_data(self):
        # Login, navigate, and download table
        self.login_and_navigate()

        success = self.router.download_table()
        if success:
            # Process the table if downloaded successfully
            extract_table_data('live_table.html', 'liveData.csv')
            guests = self.who_is_home('house_mac.csv', 'liveData.csv')
            for guest in guests:
                print(guest["Owner"])
            self.router.refresh_page()
        else:
            print("Failed to download the table. Restarting process...")
            self.router.close_driver()
            self.login = False

    def listen_for_manual_trigger(self):
        # Continuously listen for user input to trigger manual data fetch
        while True:
            user_input = input("Press 'm' for manual live data fetch: ").strip().lower()
            if user_input == 'm':
                print("Manual data fetch triggered!")
                self.manual_fetch_event.set()  # Signal manual fetch

    def who_is_home(self, house_mac, live_mac):
        # Load the CSV files into DataFrames
        house = pd.read_csv(house_mac)
        live = pd.read_csv(live_mac)

        # Perform an inner join to find common rows based on MAC ADDRESS
        merged_df = pd.merge(house, live, on='MAC Address', how='inner')

        # Select the required columns and format as a list of dictionaries
        result = merged_df[['MAC Address', 'Owner', 'IP Address']].to_dict(orient='records')

        return result


def main():
    monitoring_system = MonitoringSystem()
    monitoring_system.run()


if __name__ == '__main__':
    main()
