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
    os.system('cls')
    while True:
        print("To select an option type in it's corresponding number number:\n")
        options_list = ["1. Add item", "2. Remove item", "3. Rename item", "4. Change item count", "5. Lookup item by name", "6. List all items"]
        
        for option in options_list:
            print(option)
                
        option_select = input("\nPlease, select what you would like to do:\n")
                
        if validate_inputs(option_select):
            option_selected = options_list[int(option_select) -1]
            os.system('cls')
            print(f"\nYou selected option nr:\n{option_selected}\n")
            break
    return option_select

def selection_option_assignment(selection):
    '''
    Function first checks if option #6 was selected.
    If it was, function runs list_all_items() which does not need any additional inputs.
    And if another option was selected function asks for input of an item name. 
    With name provided function checks if item already exists on a list.
    Depending on action selected selection_option_assignment() runs corresponding function.
    '''
    inventory = SHEET.worksheet('inventory')
        
    if selection == 6:
        list_all_items(inventory.get_all_values())
    else:
        item_name_input = input('Input item name:\n')
        item_search = inventory.find(str.lower(item_name_input))
        print(f"\nYou typed: {item_name_input}\n")
        
        count_cell_value = int(inventory.cell(item_search.row, item_search.col + 1).value)
        count_cell_address = inventory.cell(item_search.row, item_search.col + 1).address
        name_cell_value = item_search.value
        name_cell_address = item_search.address
        
        if item_search != None:
            item_found = True
        else:
            item_found = False
        
        if selection == 1 and item_found == False:
            print('Run add_item()')
        elif selection == 1 and item_found == True:
            os.system('cls')
            print(f'\nItem by the name\n{item_name_input}\nis already on the list\n')
            return_or_continue(selection)
        elif selection == 2 and item_found == True:
            os.system('cls')
            print(f'You are removing {item_name_input}...')
        elif selection == 3 and item_found == True:
            os.system('cls')
            print(f'You are renaming {item_name_input}...')
        elif selection == 4 and item_found == True:
            os.system('cls')
            print(f'You are changing count of {item_name_input}..')
        elif selection == 5 and item_found == True:
            os.system('cls')
            print(f'You are searching for {item_name_input}...')
            update_cell_data(count_cell_value, count_cell_address, name_cell_value, name_cell_address, selection)
        elif selection in range(2, 6) and item_found == False:
            os.system('cls')
            print('Item not found.\n')
            return_or_continue(selection)

def validate_inputs(selection):
    '''
    Function verifies if user inputs are integers in range of 1-6 (including 6)
    '''
    try:       
        if int(selection) not in range(1, 7):
            raise IndexError(f"only numbers between 1 and 6 are accepted.")
        elif type(selection) == int():
            raise ValueError()
    except IndexError as e:
        os.system('cls')
        print(f"Invalid selection: {e}. You selected: {selection}\nTry another option\n")
        return False
    except ValueError:
        os.system('cls')
        print(f"Invalid selection: letters and special characters are not permitted. You inserted: {selection}\nPlease, use numbers to select options\n")
        return False
    return True

def return_or_continue(selection):
    '''
    In case selection_option_assignment() does not find a item_name used by a user
    this function will allow user to input new item_name or otherwise return to main menu.    
    '''
    answer = input("Do you want to try with different item (y/n)?\n").lower()
    if answer == 'n':
        os.system('cls')
        main()
    elif answer == 'y':
        selection_option_assignment(selection)
    elif answer != 'y' or 'n':
        print('\nPlease select:\n"y" for yes\nor\n"n" for no\n')
        return_or_continue(selection)

def update_cell_data(count_cell_value, count_cell_address, name_cell_value, name_cell_address, selection):
    '''
    After selection_option_assignment() runs it passes cell location data for searched items.
    This function uses this data to access those cells and depending on select_action() result it will apply correct action (i.e remove item and it's count).
    '''
    if selection == 5:
        print(f"Item: {name_cell_value.upper()}\nCount: {count_cell_value}\nList address: {name_cell_address}{count_cell_address}")

def list_all_items(inventory):
    '''
    This function lists all items (including headlines for reference) currently the list
    '''
    for item in inventory:
        print(item)

def main():
    '''
    Program start function
    '''
    users_choice = int(select_action())
    selection_option_assignment(users_choice)

main()
