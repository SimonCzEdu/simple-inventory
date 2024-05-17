import gspread
import os
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
    
    return option_select

def select_item_name(selection):
    '''
    Function first asks for input of an item name. Then it checks if item already exists on a list and depending on action selected runs corresponding function.
    '''
    item_name_input = input('Input item name:\n')
    print(f"\nYour item name is: {item_name_input}\n")
    
    inventory = SHEET.worksheet('inventory')
    if inventory.find(str.lower(item_name_input)) != None:
        item_found = True
    else:
        item_found = False
    
    if selection == 1 and item_found == False:
        print('Run add_item()')
    elif selection == 1 and item_found == True:
        # os.system('cls')
        print('\nItem by that name is already on the list\n\nChoose another name:')  
    elif selection == 2 and item_found == True:
        print('Run remove_item()')
    elif selection == 3 and item_found == True:
        print('Run rename_item()')
    elif selection == 4 and item_found == True:
        print('Run change_item_count()')
    elif selection == 5 and item_found == True:
        print('Run lookup_item()')
 

def main():
    '''
    Program start function
    '''
    users_choice = int(select_action())
    if users_choice != 6:
        select_item_name(users_choice)
    else:
        print('Run. List all items')

main()
