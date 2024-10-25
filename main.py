import csv
import re
import os
import time
import math
import datetime

"""
TODO:
-- Reorder 7th/8th grade to | Time | Email | Class | Name |
-- Somehow combine the two .csv into one making sure that the time is still in order
"""

# List to store lines from the CSV file
lines = []
#file_name = 'Fai Adesso - Form Responses TEST.csv' # Test
file_name = "Fai Adesso Ottobre (Responses) - Form Responses 1.csv" # real

# Initialize grades dictionary for each color group
grades = [{}, {}, {}, {}, {}, {}]
colors = ["Rosso", "Arancione", "Giallo", "Verde", "Blu", "Viola"]
names = {}  # To store names associated with users
most_recent_user_date = {}  # To track the last date each user submitted
sus_days = {}
all_users = []
all_days = []
checking_date = ""
excluded_days = []
# checking_sus_days = False

# Variable to track the index of lines
x = -1

# ANSI color codes for terminal output
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
CYAN = "\033[36m" 
WHITE = "\033[37m"
RESET = "\033[0m"

def clear_console():
    # Clear the terminal screen based on the OS.
    # if os.name == 'nt':
    #     os.system('cls')  # Windows
    # else:
    #     os.system('clear')  # Unix/Linux
    print("FAKE CLEAR")

def color_to_number(color):
    """Convert color name to an index number for grades."""
    if color == "Rosso":
        return 0
    elif color == "Arancione":
        return 1
    elif color == "Giallo":
        return 2
    elif color == "Verde":
        return 3
    elif color == "Blu":
        return 4
    elif color == "Viola":
        return 5

def new_email(email):
    # Clean up the email address by removing the domain.
    email = re.sub('@watertown.k12.ma.us', '', email)
    return email

with open(file_name, newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)  # Skip header row
    
    for row in read:
        # if color_to_number(color) == 2 or color_to_number(color) == 5:
        #     x += 1  # Increment line index
        #     lines.append(row)  # Append the row to lines
        #     current_line = lines[x]
        #     user = new_email(current_line[1])  # Extract and clean email
        #     current_date = current_line[0][:-8]  # Extract date from current line
        #     color = row[2]  # Extract the color associated with the user
        #     class_number = int(color_to_number(color))  # Convert color to index
        #     # Convert date string to datetime object
        #     datetime_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
        #     week_number = datetime_obj.weekday()  # Get the weekday (Monday=0)
            
        #     # Skip weekends (Saturday=5, Sunday=6)
        #     if week_number == 5 or week_number == 6 or current_date in excluded_days:
        #         continue
        #     if user not in all_users: # Check if the user is unique
        #         all_users.append(user)
        #     if current_date not in all_days:
        #         all_days.append(current_date)
        # else:
        x += 1  # Increment line index
        lines.append(row)  # Append the row to lines
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        current_date = current_line[0][:-8]  # Extract date from current line
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index
        # Convert date string to datetime object
        datetime_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
        week_number = datetime_obj.weekday()  # Get the weekday (Monday=0)
        row.clear()
    
        
        # Skip weekends (Saturday=5, Sunday=6)
        if week_number == 5 or week_number == 6 or current_date in excluded_days:
            continue
        if user not in all_users: # Check if the user is unique
            all_users.append(user)
        if current_date not in all_days:
            all_days.append(current_date)

with open(file_name, newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)  # Skip header row
    x = -1
    today_users = []
    last_checked_date = ""  # Track the date to detect changes
    for row in read:
        x += 1  # Increment line index
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        current_date = str(current_line[0][:-8])  # Extract date from current line
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index

        # If the date has changed, process the previous day and reset `today_users`
        if last_checked_date and current_date != last_checked_date:
            # Check if the number of today's users is less than half of all users
            if len(today_users) / len(all_users) <= 0.5:
                sus_days[last_checked_date] = int(len(today_users) / len(all_users) * 100)
            # Reset `today_users` for the new day
            today_users = []  # Reset for the new day

        if user not in today_users:
            today_users.append(user)

        # Update the last_checked_date for the next iteration
        last_checked_date = current_date

    # Handle the last date after the loop ends
    if last_checked_date and len(today_users) / len(all_users) <= 0.5:
        sus_days[last_checked_date] = int(len(today_users) / len(all_users) * 100)




x = -1

# Assuming `all_days` is a list of days and `sus_days` is a dictionary with day as key
days = len(all_days)  # Get the length of `all_days` list as an integer
excluded_days = []    # List to keep track of excluded days

for day_key in list(sus_days.keys()):

    # Convert date string to datetime object
    datetime_obj = datetime.datetime.strptime(day_key, "%m/%d/%Y")
    week_number = datetime_obj.weekday()  # Get the weekday (Monday=0)
        
    # Skip weekends (Saturday=5, Sunday=6)
    if week_number == 5 or week_number == 6:
        continue

    while True:
        

        clear_console()

        print(f"{GREEN}{day_key}{PURPLE} may be a day that there was no school, or the teacher was absent. Only {GREEN}{sus_days[day_key]}{PURPLE} percent of people responded on this day.")
        override_sus_days = input("Do you want to exclude this day? (y/N)\n" + GREEN).strip().lower()
        
        if override_sus_days in ["no", "n", ""]:
            break
        elif override_sus_days in ["yes", "y"]:
            excluded_days.append(day_key)
            days -= 1
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
        


# Read the CSV file with form responses
with open(file_name, newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)  # Skip header row
    for row in read:
        x += 1  # Increment line index
        lines.append(row)  # Append the row to lines
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        if user not in most_recent_user_date:
            most_recent_user_date[user] = None  # Initialize date tracking
        
        current_date = current_line[0][:-8]  # Extract date from current line
        
        if not user or len(user) == 0:
            continue  # Skip invalid or empty emails
        
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index
        
        # Count non-empty responses for the user
        i = 0
        for j in range(4, 8):  # Columns 4 to 8 are question responses
            if row[j] != '':
                i += 1
        
        # Convert date string to datetime object
        datetime_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
        week_number = datetime_obj.weekday()  # Get the weekday (Monday=0)
        
        # Skip weekends (Saturday=5, Sunday=6)
        if week_number == 5 or week_number == 6 or current_date in excluded_days:
            continue
        
        # Skip if user has already submitted for this date
        if most_recent_user_date[user] == current_date:
            continue
        
        # Skip if day is in excuded days list
        if current_date in excluded_days:
            continue

        # Update grades for the user
        if user in grades[color_to_number(color)]:  # If user already exists
            grades[color_to_number(color)][user] += i  # Increment points
        else:  # New user
            grades[color_to_number(color)][user] = i  # Set points
        
        # Update the most recent date for this user
        most_recent_user_date[user] = current_date
        names[user] = current_line[3]  # Store the user's name

# Display grades
clear_console()
print(GREEN)
for y in range(len(grades)):
    current_color = colors[y]  # For display purposes
    print(PURPLE + current_color + ":\n" + GREEN)
    for i, key_at_position in enumerate(grades[y].keys()):  # Access grades by index
        # Calculate percentage score
        #percentage = math.ceil(grades[y][key_at_position] / 5 / int(days) * 100)
        percentage = (int(grades[y][key_at_position]) / (int(days) * 5)) * 100
        print(names[key_at_position] + " / " + key_at_position + PURPLE + " --> " +
              GREEN + str(grades[y][key_at_position]) + "/" + str(int(days) * 5) + 
              " -- " + str(int(percentage)) + "%\n")

# 6th grade version      
# percentage = (int(grades[y][key_at_position]) / (int(days) * 3)) * 100
# print(names[key_at_position] + " / " + key_at_position + PURPLE + " --> " +
#     GREEN + str(grades[y][key_at_position]) + "/" + str(int(days) * 3) + 
#     " -- " + str(int(percentage)) + "%\n")
