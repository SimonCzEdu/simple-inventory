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
    while True:
        print("\nTo select an option type-in it's corresponding number number:\n")
        options_list = ["1. Add item", "2. Remove item", "3. Rename item", "4. Change item count", "5. Lookup item by name", "6. List all items"]
        
        for option in options_list:
            print(option)
                
        option_select = input("\nPlease, select what you would like to do:\n")
                
        if validate_inputs(option_select):
            option_selected = options_list[int(option_select) -1]
            print(f"\nYou selected option nr: {option_selected}\n")
            break
    return option_select

def select_item_name(selection):
    '''
    Function first asks for input of an item name. Then it checks if item already exists on a list and depending on action selected runs corresponding function.
    '''
    item_name_input = input('Input item name:\n')
    print(f"\nYou typed: {item_name_input}\n")
    
    inventory = SHEET.worksheet('inventory')
    if inventory.find(str.lower(item_name_input)) != None:
        item_found = True
    else:
        item_found = False
    
    if selection == 1 and item_found == False:
        print('Run add_item()')
    elif selection == 1 and item_found == True:
        os.system('cls')
        print('\nItem by that name is already on the list\n')
        return_or_continue(selection)
    elif selection == 2 and item_found == True:
        print('Run remove_item()')
    elif selection == 3 and item_found == True:
        print('Run rename_item()')
    elif selection == 4 and item_found == True:
        print('Run change_item_count()')
    elif selection == 5 and item_found == True:
        print('Run lookup_item()')   
    elif selection in range(2, 6) and item_found == False:
        print('Item not found.\n')
        return_or_continue(selection)

def validate_inputs(selection):
    try:       
        if int(selection) not in range(1, 7):
            raise IndexError(f"only numbers between 1 and 6 are accepted.")
        elif type(selection) == int():
            raise ValueError(f"letters are not permitted.")
    except IndexError as e:
        os.system('cls')
        print(f"Invalid selection: {e}. You selected: {selection}\nTry another option\n")
        return False
    except ValueError as e2:
        os.system('cls')
        print(f"Invalid selection: {e2}. You selected: {selection}\nTry another option\n")
        return False
    return True

def return_or_continue(selection):
    answer = input("Do you want to try with different item (y/n)?\n").lower()
    if answer == 'n':
        main()
    elif answer == 'y':
        select_item_name(selection)
    elif answer != 'y' or 'n':
        print('Answer can only be y for yes or n for no')
        return_or_continue(selection)

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
