import csv
import requests

# Replace CSV_URL with the URL of the CSV you want to download
CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=W1U7T09FFM4DY97N'

# Path where you want to save the downloaded CSV file on your Mac
SAVE_PATH = r'//Users/alanjackson/Environments/alphaVantageAPI/AV_Stock_Indexes.csv'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    
    # Write the CSV content to a local file
    with open(SAVE_PATH, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        for row in cr:
            csv_writer.writerow(row)

print(f'CSV file has been saved to: {SAVE_PATH}')
