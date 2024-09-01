
# robin_stocks docs --> https://robin-stocks.readthedocs.io/en/latest/quickstart.html
# python interpreter path: /Users/alanjackson/Environments/alphaVantageAPI/myEnv/bin/python

import AVcredentials
import csv
import robin_stocks.robinhood as r

login = r.login("aj96818@gmail.com", AVcredentials.rh_pw)
my_stocks = r.build_holdings()

# for key,value in my_stocks.items():
#     print(key,value)

def export_dict_to_csv(data, file_path):
    """
    Exports a dictionary to a CSV file.

    Parameters:
        data (dict): The dictionary containing stock data.
        file_path (str): The path where the CSV file will be saved.
    """
    if not data:
        raise ValueError("The data dictionary is empty.")

    # Get the field names from the first entry in the dictionary
    first_key = next(iter(data))
    fieldnames = ['symbol'] + list(data[first_key].keys())

    # Open the CSV file for writing
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header (field names)
        writer.writeheader()

        # Write the data rows
        for symbol, attributes in data.items():
            row = {'symbol': symbol}  # Add the stock symbol to the row
            row.update(attributes)     # Add the rest of the attributes
            writer.writerow(row)       # Write the row to the CSV file


# Call the function to export the dictionary to a CSV file
# export_dict_to_csv(my_stocks, '/Users/alanjackson/Environments/alphaVantageAPI/RobinhoodPortfolio.csv')
