import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
# the next 3 lines are to check if the API is working

# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)

def get_sales_data():
    """
    Get sales figures input from the user
    """

    """
    We wrap the func in a while loop so that everytime the data
    is not valid it repeats the loop without breaking the program.
    If the data is valid from validate_data func, the loop will break.
    """
    while True:
        print("Please enter the sales data from the last market")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
        # the nex print statement is only to check 
        # print(f"The data provided is {data_str}")

        # The split method returns the broken up values as a list
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data        



def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 numbers.
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True       


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    # append_row is a method from gspread
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    -  Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    pprint(stock_row)




def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome To Love sandwiches Data Automation")
main()