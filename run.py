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


def update_worksheet(data, worksheet):
    """
    Update worksheet, add new row with corresponding list of data.
    """
    print(f"Updating {worksheet} Worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} Worksheet Updated Successfully.\n")



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
    
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)


    return surplus_data  


def get_last_5_entries_sale():
    """
    Collects columns of data from slaes worksheet, collecting
    the last 5 entries for each sandwich and returns the data as a list of lists.
    """

    sales = SHEET.worksheet("sales")

    # the col_values() is a methos from gspread returning the relevant col.
    # column = sales.col_values(3)
    # print(column)

    columns =[]
    for ind in range(1, 7):
        column = sales.col_values(ind)
        # we use the slice method here cause we only need the last 5 columns.
        columns.append(column[-5:])

    return columns    


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """    
    print("Calculating stock data ...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        # or sum(int_column) / 5, because we alreday know that the length is 5 
        # as we sliced it before.
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


  



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sale()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    return stock_data


print("Welcome To Love sandwiches Data Automation")
stock_data = main()

def get_stock_values(data):
    headings = SHEET.worksheet("stock").row_values(1)


    print("Make the following numbers of sandwiches for next market:\n")
    
    return {heading: data for heading, data in zip(headings, data)}  

stock_values = get_stock_values(stock_data)
print(stock_values)








