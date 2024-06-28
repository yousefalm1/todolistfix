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
SHEET = GSPREAD_CLIENT.open('to_do_list')

to_do_list_worksheet = SHEET.worksheet('Sheet1')

# creates an empty list to store the tasks the user inputs
to_do_list = []


def display_welcome_message():
    """
    Function to display a welcome message
    """
    print("Welcome to your own personal TO-DO List\n")


def add_task():
    """
    Function to add a task to the to-do list
    """
    # try block to catch any potential errors
    try:
        # User enters the task and the task the user inputed is stored in "task"
        task = input("Enter the task:\n")

        # User enter due date for task which is optional
        due_date = input("Enter the due date (optional) (__/__/__):\n")

        # creates a dictionary to show the task and the due date to add to the local to-do list
        task_details = {
            "Task": task,
            "Due Date": due_date if due_date else "No due date"
        }

        # Append the task detials to the local to-do list
        to_do_list.append(task_details)

        # Add task and due date to google sheets
        # Create a list with task and due date
        task_data = [task, due_date if due_date else "No due date"]
        # By using append rows to add a new row to the google
        to_do_list_worksheet.append_rows([task_data])

        # Print Success message
        print(
            f"Task: '{task}' has been successfully added to the to-do list and Google Sheets.\n")

    #  if an excpetion is raised within the try block it will print "An error occured"
    except Exception as e:
        print(f"An error occured: {e}")


def remove_task():
    """
    Function to remove a task from the to-do list by index
    """
    try:
        # Display the current to-do list with indices
        print("Current To-Do List:\n")
        # A for loop to iterate through "to_do_list" and prints each task's index and task name
        for index, task_details in enumerate(to_do_list):
            print(f"{index + 1}. {task_details['Task']}")

        # User is told to enter the index of the task they want to remove
        index_to_remove = input("Enter the index of the task to remove:\n")
        # Check if the what the user inputted is valid (using isdigit which makes sure the input is a number)
        if index_to_remove.isdigit():
            # Converts what the user inputted to an integer then adjust it to start at 0
            index_to_remove = int(index_to_remove) - 1

            # len(to_do_list) calculates the number of tasks and returns an integer
            # 0 <= index_to_remove checks if the "index_to_remove" is greater than or equal to 0 to make sure the index is not negative
            # index_to_remove < len(to_do_list) checks if "index_to_remove" is less than the length of the to_do list to make sure the index is not greater than or equal to the number of tasks
            if 0 <= index_to_remove < len(to_do_list):
                task_to_remove = to_do_list[index_to_remove]["Task"]

                # Using findall to search the google sheets for the task to remove
                task_rows = to_do_list_worksheet.findall(task_to_remove)

                # A loop that goes over all the matching rows
                for row in task_rows:
                    # Deletes the entire row in google sheets
                    to_do_list_worksheet.delete_rows(row.row)
                # Delete task from the local list
                del to_do_list[index_to_remove]

                print(
                    f"Task '{task_to_remove}' has been successfully been removed\n")
            else:
                print("Invalid Index. Please Enter a valid index\n")
        # This is raised when the converting to an integer fails
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
    # This catches an unexpected error
    except Exception as e:
        print(f"An error occurred: {e}")


def display_list():
    """
    Function to display the to-do list
    """
    try:
        # Checks if the "to_do_list" is empty, if it is print the statement below
        if not to_do_list:
            print("Your to-do list is empty.\n")
        # If "to_do_list" is not empty the code below will run
        else:
            print("To-DO List:\n")
            # This keeps track of the task numbers in the "to_do_list"
            count = 1
            # This for loop iterates over each item the user submited in the "to_do_list" and assigns it to "task"
            for task in to_do_list:
                # Inside the loop the print line it prints "1. Task 1", "2. Task 2" ....
                print(f"{count}. {task}")
                # After printing each task the count goes up by 1 for the next task
                count += 1
    except Exception as e:
        print(f"An error occured: {e}")


def quit():
    """
    Quit to-do list function
    """
    print("You have quit the to-do list")


def main():
    """
    Function to run the to-do list
    """
#  Creates an infinite loop until the user chooses to quits
    try:
        while True:
            display_welcome_message()
            # Print the options so the user knows what to pick
            print("Menu:\n")
            print("1. Add a task")
            print("2. Remove a task")
            print("3. Display to-do-list")
            print("4. Quit\n")

            # The number the user input will be assigned to "Choice"
            choice = input("Enter Your choice:\n")

            # Checks what number the user inputed and calls the function linked to that number
            if choice == "1":
                # Calls the fuction to add a task
                add_task()
            elif choice == "2":
                # Calls the fuction to remove a task
                remove_task()
            elif choice == "3":
                # Calls the fuction to display tasks
                display_list()
            elif choice == "4":
                # Exit the loop and quit
                quit()
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


main()
