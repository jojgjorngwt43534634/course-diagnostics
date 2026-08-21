import sys

products = []

def main_menu():
        print('----------------------------------------------')
        print('--- Welcome to Inventory Management System ---')
        print('----------------------------------------------')
        print('[1] Add a Product')
        print('[2] Remove a Product')
        print('[3] Update Quantity')
        print('[4] Display Inventory')
        print('[5] Save Current Inventory')
        print('[6] Exit')
        try:
            option = int(input('\nWhat would you like to do: '))
            if option == 1:
                add_product()
            elif option == 2:
                remove_product()
            elif option == 3:
                update_modify()
            elif option == 4:
                display_record()
            elif option == 5:
                save_file()
            elif option == 6:
                goodbye()
            else:
                print('Choose a Number between 1-6')
        except ValueError:
            print('Please enter a valid number.')

def get_valid_float(prompt_text):
    while True:
        try:
            value = float(input(prompt_text))
            if value < 0:
                print("Value cannot be negative. Please try again.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_int(prompt_text):
    while True:
        try:
            value = int(input(prompt_text))
            if value < 0:
                print("Value cannot be negative.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def add_product():
    name = input('Enter Product Name: ').strip()
    if not name:
        print("Product name cannot be empty.")
        return

    quantity = get_valid_int('Enter Quantity: ')
    price = get_valid_float('Enter Price: ')
    
    total_cost = quantity * price
    
    record = { 
        'name': name,
        'quantity': quantity,
        'price': price,
        'total': total_cost,
        }
        
    products.append(record)
    print(f'Product "{name}" Added Successfully!')

def remove_product():
    search_name = input('Enter Product Name to remove: ').strip()
    
    found = False
    for product in products:
        # Check if names match (case insensitive)
        if product['name'].lower() == search_name.lower():
            products.remove(product)
            print('Record has been removed.')
            found = True
            break
            
    if not found:
        print('Product not found.')

def update_modify():
    search_name = input('Enter Product Name to Modify: ').strip()
    
    found = False
    for product in products:
        if product['name'].lower() == search_name.lower():                    
            print(f"\nCurrent Quantity: {product['quantity']}")
            
            try:
                new_qty_input = input("Enter New Quantity (press Enter to keep current): ")
                if new_qty_input == "":
                    new_qty = product['quantity']
                else:
                    new_qty = int(new_qty_input)
                
                product['quantity'] = new_qty
                product['total'] = product['quantity'] * product['price']
                                    
                print("Record Updated Successfully!")
            except ValueError:
                print("Invalid quantity entered. Update cancelled.")
            
            found = True
            break
        
    if not found:
        print('Product not found.')

def display_record():
    if not products:
        print("\nInventory is empty.")
        return

    print('\n-----------------------------------------------------------------------')
    print(f"|{'Product Name':<43} | {'Qty':<8} | {'Price':<5} | {'Total':<8}")
    print('-----------------------------------------------------------------------')
    
    for product in products:
        print(f"|{product['name']:<43} | {product['quantity']:<8} | {product['price']:<5} | {product['total']:.2f}")

    print('----------------------------------------------------------------------')
        
def save_file():
    if not products:
        print("No products to save.")
        return

    filename = input('Enter filename to save (e.g. data.txt): ')
    try:
        with open(filename, "w") as f:
            for product in products:
                line = f"{product['name']},{product['quantity']},{product['price']},{product['total']}\n"
                f.write(line)
        print('Saved successfully')
    except Exception as e:
        print(f'Error saving file: {e}')
        
def goodbye():
    print('\nGoodbye!')
    sys.exit()

while True:
    main_menu()

    while True:
        try:
            again = input('\nDo you want to return to Main Menu? (y/n): ')
            if again.lower() == 'y' and again.upper() == 'Y':
                break
            elif again.lower() == 'n' or again.upper() == 'N':
                goodbye()
            else:
                print('Letters Y OR N')
        except ValueError:
            print('Letters Y OR N')