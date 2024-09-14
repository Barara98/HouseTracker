from bs4 import BeautifulSoup
import csv
import os


def extract_table_data(html_file, csv_output):
    # Load the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find the <tbody> element (assuming there's only one in the file)
    tbody = soup.find('tbody')

    if not tbody:
        print(f"No <tbody> found in {html_file}")
        return

    # Find all the rows <tr> inside the <tbody>
    rows = tbody.find_all('tr')

    # Open a file to save the extracted data (as CSV for structured storage)
    with open(csv_output, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header for the CSV
        writer.writerow(['Status', 'MAC Address', 'IP Address'])

        # Loop through each row (<tr>)
        for row in rows:
            # Get all <td> elements in the row
            tds = row.find_all('td')

            # Ensure there are enough <td> elements
            if len(tds) >= 6:
                # Extract the 4th <td> for Status, 5th <td> for MAC, and 6th <td> for IP
                status = tds[3].get_text(strip=True)
                mac = tds[4].get_text(strip=True)
                ip = tds[5].get_text(strip=True)

                # Write the extracted data to the CSV file
                if status == 'on':
                    writer.writerow([status, mac, ip])

                    # Optionally print the data for debugging
                    # print(f'Status: {status}, MAC: {mac}, IP: {ip}')

    print(f"Data extraction complete. Check '{csv_output}' for the results.")
    # delete live_table.html
    os.remove(html_file)
    print(f"Deleted '{html_file}'")
