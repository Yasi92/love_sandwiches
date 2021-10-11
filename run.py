import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

<<<<<<< HEAD

=======
>>>>>>> 45ccb3ae0baf60e056df38da776c1ce358ff34f9
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)
<<<<<<< HEAD
print('hello')


=======

print("hey")
>>>>>>> 45ccb3ae0baf60e056df38da776c1ce358ff34f9
