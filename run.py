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
        print("\nTo select an option type in it's corresponding number number:\n")
        options_list = ["1. Add item", "2. Remove item", "3. Rename item", "4. Change item count", "5. Lookup item by name", "6. List all items"]
        
        for option in options_list:
            print(option)
                
        option_select = input("\nPlease, select what you would like to do:\n")
                
        if validate_selection_inputs(option_select):
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
    Depending on action selected selection_option_assignment() will execute corresponding code.
    '''
    inventory = SHEET.worksheet('inventory')
        
    if selection == 6:
        list_all_items(inventory.get_all_values())
    else:
        def name_input(input):
            '''
            This function searches worksheet for the user inputs and returns them to the terminal.
            If item was found name_input() will provide us with cell data (address, value).
            We will need this data later to modify worksheet data.
            If input is not present in the worksheet name_input() will return none value.
            That none value can later be used in the "if/else if" statement to select option to be run.
            '''
            item_search = inventory.find(str(input))
            print(f"\nYou typed: {input}\n")
            return item_search
            
        item_name_input = input('Input item name:\n')
        item_search_result = name_input(item_name_input)
        if item_search_result != None:
            count_cell_value = int(inventory.cell(item_search_result.row, item_search_result.col + 1).value)
            count_cell_address = inventory.cell(item_search_result.row, item_search_result.col + 1).address
            name_cell_value = item_search_result.value
            name_cell_address = item_search_result.address
        
        if selection == 1 and item_search_result == None:
            while True:
                print(f"Adding {item_name_input} to the list...")
                new_item_count = input(f"The count of {item_name_input}:\n")
                if count_input_validation(new_item_count):
                    entered_item_count = int(new_item_count)
                    inventory.append_row([item_name_input, entered_item_count])
                    break
            main()        
        elif selection == 1 and item_search_result != None:
            os.system('cls')
            print(f'\nItem by the name\n{item_name_input}\nis already on the list\n')
            main()
        elif selection == 2 and item_search_result != None:
            os.system('cls')
            print(f'You are removing {item_name_input}...')
            inventory.delete_rows(item_search_result.row)
            print(f'{item_name_input} removed.')
            main()            
        elif selection == 3 and item_search_result != None:
            os.system('cls')
            print(f'You are renaming {item_name_input}...\n')
            new_name = input('How would you like to rename this item:\n')
            if name_input(new_name) == None:
                print(f"Renaming {item_name_input} to {new_name}")
                inventory.update_acell(name_cell_address, new_name)
                print(f"Renamed {item_name_input}\nNew name: {new_name}")
                main()
            else:
                print("Item like this already exists.")
                main()
        elif selection == 4 and item_search_result != None:
            while True:                          
                print(f'You are changing count of {item_name_input}...')
                new_count = input('Input new count value:\n')
                if count_input_validation(new_count):
                    value_of_new_count = int(new_count)
                    inventory.update_acell(count_cell_address, value_of_new_count)
                    print(f"Count of {item_name_input} changed to: {value_of_new_count}")
                    break
            main()                
        elif selection == 5 and item_search_result != None:
            os.system('cls')
            print(f'You are searching for {item_name_input}...\n')
            print(f"Item: {name_cell_value.upper()}\nCount: {count_cell_value}\nList address: {name_cell_address}{count_cell_address}\n")
            main()
        elif selection in range(2, 6) and item_search_result == None:
            os.system('cls')
            print('Item not found.\n')
            main()

def count_input_validation(count):
    try:
        int(count)
    except ValueError as e:
        os.system('cls')
        print(f"Your input has to be a whole number i.e. 10. Letters/strings or floats i.e. 1.1 will not be accepted.\nTry again")
        return False
    return True

def validate_selection_inputs(selection):
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

# def return_or_continue(selection):
    '''
    In case selection_option_assignment() does not find the item_name used by a user
    this function will allow user to input new item_name or otherwise return to main menu.    
    '''
    answer = input("Would you like to modify different item? If you chose (N or n), you will return to the main menu.\nIf you chose (Y or y), you can retype item you whish to modify.\n").lower()
    if answer == 'n':
        os.system('cls')
        main()
    elif answer == 'y':
        selection_option_assignment(selection)
    elif answer != 'y' or 'n':
        print('\nPlease select:\nY for yes\nor\nN for no\n')
        return_or_continue(selection)

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
