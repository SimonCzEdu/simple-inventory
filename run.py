import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('simple-inventory')

def select_action():
    '''
    Function input from a user will decide which action is taken.
    '''
    
    print("\nTo select an option type-in it's corresponding number number:\n")
    options_list = ["1. Add item", "2. Remove item", "3. Rename item", "4. Change item count", "5. List all items", "6. Look up items by name"]
    
    for option in options_list:
        print(option)
                    
    option_select = input("\nPlease, select what you would like to do: ")    
    option_selected = str(options_list[int(option_select) -1])
    
    print(f"\nYou selected option nr: {option_selected}\n")
    
    return option_selected

users_choice = select_action()
if users_choice == "1. Add item":
    print('Run add func.')
elif users_choice == "2. Remove item":
    print('Run remove func.')
elif users_choice == "3. Rename item":
    print('Run rename func.')
elif users_choice == "4. Change item count":
    print('Run change func.')
elif users_choice == "5. List all items":
    print('Run list func.')
elif users_choice == "6. Look up items by name":
    print('Run look up func.')
