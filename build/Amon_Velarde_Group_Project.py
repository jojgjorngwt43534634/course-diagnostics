import sys
import os

students = []

print('STUDENT RECORDS.')
print('Choose to make a new file or go through existing records: \n')

print('------------------------------')
print('         File Options         ')
print('------------------------------')

def first_option():
    while True:
        print('\n[1] New File')
        print('[2] Existing File')
        try:
            choice = int(input('\nWhat would you like to do: '))

            if choice == 1:
                new_file()
                break
            elif choice == 2:
                exist_file()
                break
            else:
                print('Choose a Number between 1-2')
            
        except ValueError:
            print('Not a value')
            break

def new_file():
    while True:
        print('------------------------------')
        print('     Main Menu - New File     ')
        print('------------------------------')
        print('[1] Add a Student Record')
        print('[2] Remove a Student Record')
        print('[3] Modify Records')
        print('[4] Display Current Records')
        print('[5] Save Current Records to a File')
        print('[6] Search through Current Records')
        print('[7] Exit')
        try:
            option = int(input('\nWhat would you like to do: '))
            if option == 1:
                add_student()
            elif option == 2:
                remove_student()
            elif option == 3:
                modify()
            elif option == 4:
                display_record()
            elif option == 5:
                save_file()
            elif option == 6:
                search_record()
            elif option == 7:
                goodbye()
                break
            else:
                print('Choose a Number between 1-7')
                
        except ValueError:
            print('Not a Value')
            
def get_valid_grade(prompt_text):
    while True:
        try:
            grade = float(input(prompt_text))
            if grade < 0:
                print("Grade cannot be negative. Please try again.")
            else:
                return grade
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_modify_grade(prompt, current_val):
    while True:
        user_input = input(f"{prompt} ({current_val}): ")
        
        if not user_input:
            return current_val
            
        try:
            grade = float(user_input)
            if grade < 0:
                print("Grade cannot be negative. Please try again.")
            else:
                return grade
        except ValueError:
            print("Invalid input. Please enter a positive number.")

            
def add_student():
    print('\n---Add a Student Record---')
    
    full_input = str(input('Enter Name (Lastname Firstname): '))
    parts = full_input.split()
    
    if len(parts) >= 2:
        ln = parts[0]
        fn = parts[1]
        
        sec = str(input('Enter section: '))
        
        print('Enter grades below')
        
        q1 = get_valid_grade('Quiz 1: ')
        q2 = get_valid_grade('Quiz 2: ')
        q3 = get_valid_grade('Quiz 3: ')
            
        ave = (q1 + q2 + q3)/3 
        
        record = { 
            'last': ln,
            'first': fn,
            'section':sec,
            'q1':q1,
            'q2': q2,
            'q3': q3,
            'average': ave
            }
            
        students.append(record)
        print('Record Added Successfully!')

    else:
        print("Invalid format. Please type 'Lastname Firstname'")
            
def remove_student():
    try:
        full_input = str(input('Enter Name to remove (Lastname Firstname): '))
        
        parts = full_input.split()
        
        if len(parts) >= 2:
            search_ln = parts[0]
            search_fn = parts[1]
            
            found = False
            for student in students:
                if student['last'] == search_ln and student['first'] == search_fn:
                    students.remove(student)
                    print('Record has been removed.')
                    found = True
                    break
                
            if found == False:
                print('Student not found')
        else:
            print("Invalid format. Please type 'Lastname Firstname' with a space.")
            
    except ValueError:
        print('Error removing')
            
def modify():
    try:
        full_input = str(input('Enter Name to Modify (Lastname Firstname): '))
        
        parts = full_input.split()
        
        if len(parts) >= 2:
            search_ln = parts[0]
            search_fn = parts[1]
    
            found = False
            for s in students:
                if s['last'] == search_ln and s['first'] == search_fn:
                    print(f"\nEditing record for {s['first']} {s['last']}")
                    
                    print("Enter new Info (Press Enter to keep current):")
                    
                    s['last'] = input(f"New Last Name ({s['last']}): ") or s['last']
                    s['first'] = input(f"New First Name ({s['first']}): ") or s['first']
                    s['section'] = input(f"New Section ({s['section']}): ") or s['section']
                    
                    print("Enter new grades (Press Enter to keep current grade):")
                    
                    s['q1'] = get_modify_grade("Quiz 1", s['q1'])
                    s['q2'] = get_modify_grade("Quiz 2", s['q2'])
                    s['q3'] = get_modify_grade("Quiz 3", s['q3'])
                
                    s['average'] = (s['q1'] + s['q2'] + s['q3']) / 3
                    print("Record Updated Successfully!")
                    found = True
                    break
            
            if not found:
                print('Student not found.')
        else:
            print("Invalid format.")
            
    except ValueError:
            print('Error')
            
def display_record():
        print('\n---------------------------------------------------------------------')
        print('Last Name      First Name      | Section | Q1   | Q2   | Q3   | Average')
        print('-----------------------------------------------------------------------')
    
        for s in students:
            print(f"{s['last']:<14} {s['first']:<15} | {s['section']:<7} | {s['q1']:<4} | {s['q2']:<4} | {s['q3']:<4} | {s['average']:.2f}")

            print('----------------------------------------------------------------------')
            
def save_file():
    filename = str(input('Enter filename to save (e.g. data.txt): '))
    try:
        f = open(filename, "w")
        for s in students:
            line = f"{s['last']},{s['first']},{s['section']},{s['q1']},{s['q2']},{s['q3']},{s['average']}\n"
            f.write(line)
        f.close()
        print('Saved successfully')
    except:
        print('Error saving file')
        
def search_record():
    try:
        full_input = str(input('\nEnter Name to search (Lastname Firstname): '))
    
        parts = full_input.split()
    
        if len(parts) >= 2:
            search_ln = parts[0]
            search_fn = parts[1]
    
            found = False
        for s in students:
            if s['last'] == search_ln and s['first'] == search_fn:
                print('\nFOUND:')
                print('---------------------------------------------------------------------')
                print('Last Name      First Name      | Section | Q1   | Q2   | Q3   | Average')
                print('---------------------------------------------------------------------')
                print(f"{s['last']:<14} {s['first']:<15} | {s['section']:<7} | {s['q1']:<4} | {s['q2']:<4} | {s['q3']:<4} | {s['average']:.2f}")
                print('---------------------------------------------------------------------')
                
                found = True
                break
            
        if not found:
            print('Student not found')

    except NameError:
        print("Invalid format. Please type 'Lastname Firstname'")
    
def exist_file():
    filename = str(input('\nEnter filename to load (e.g. data.txt): '))
    
    if not os.path.exists(filename):
        print("File not found!")
        return

    try:
        students.clear() 
        f = open(filename, "r")
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 7:
                record = {
                    'last': parts[0],
                    'first': parts[1],
                    'section': parts[2],
                    'q1': float(parts[3]),
                    'q2': float(parts[4]),
                    'q3': float(parts[5]),
                    'average': float(parts[6])
                }
                students.append(record)
        f.close()
        print("Records loaded successfully!")
        new_file()
    except Exception as e:
        print(f"Error loading file: {e}")
        
def goodbye():
        print('\nGoodbye!')
        input('Please Enter to Exit... ')
        sys.exit()

first_option()

again = input('\nDo you want to go back to the Main Menu (y/n): ')
if again.lower() == 'y':
   new_file()
else:
   goodbye()