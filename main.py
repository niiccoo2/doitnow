import csv
import re
import os
import time
import math
import datetime

"""
TODO:
- Limit questions for 6th grade Giallo/Viola.
- Implement a calendar feature to track teacher attendance
OR
- Use a percentage and ask the teacher if you want to not grade for that day.
"""

# List to store lines from the CSV file
lines = []

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
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Unix/Linux

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

with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)  # Skip header row
    
    for row in read:
        x += 1  # Increment line index
        lines.append(row)  # Append the row to lines
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        current_date = current_line[0][:-8]  # Extract date from current line
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index
        if user not in all_users: # Check if the user is unique
            all_users.append(user)
        if current_date not in all_days:
            all_days.append(current_date)
with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)  # Skip header row
    x=-1
    today_users = []
    for row in read:
        x += 1  # Increment line index
        lines.append(row)  # Append the row to lines
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        current_date = str(current_line[0][:-8])  # Extract date from current line
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index
        if checking_date == current_date:
            checking_date = current_date
            if int(all_users/2) >= today_users:
                sus_days[current_date] = int(today_users/int(all_users/2)*100)
            today_users = []
            # checking_sus_days = False
            today_users.append(user)
        else:
            today_users.append(user)



x = -1


while True:
    clear_console()
    #days = input(GREEN+"Benvenuto! Quanti giorni di 'Fai adesso' stai correggendo?\n\n--> "+PURPLE) 
    days = str(len(all_days))

    # if days.isnumeric():
    #     break
    #clear_console()
    #print(RED+"Enter a number.")
    #time.sleep(3)
    for i in range(len(sus_days.keys())):
        clear_console()
        while True:
            time.sleep(1)
            print(str(sus_days.keys[i], "may be a day that there was no school, or the teacher was absent. Only", sus_days[sus_days.keys()[i]]), "percent of people responed on this day.")
            override_sus_days = input("Do you want to include this day?\n").lower() 
            if override_sus_days == "no" or override_sus_days == "n":
                continue
            if override_sus_days == "yes" or override_sus_days == "y":
                excluded_days.append(sus_days.keys[i])
                days-=1
            else:
                print("Invalid input.")
                i-=1


# Read the CSV file with form responses
with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
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
        for j in range(3, 8):  # Columns 3 to 7 are question responses
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
        
        # Update grades for the user
        if user in grades[color_to_number(color)]:  # If user already exists
            grades[color_to_number(color)][user] += i  # Increment points
        else:  # New user
            grades[color_to_number(color)][user] = i  # Set points
        
        # Update the most recent date for this user
        most_recent_user_date[user] = current_date
        names[user] = current_line[8]  # Store the user's name

# The following section is commented out but appears to be duplicate code
# for processing a different CSV file.


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
              " -- " + str(percentage) + "\n")
import csv
import re
import os
import time
import math
import datetime

"""
TODO:
- Limit questions for 6th grade Giallo/Viola.
- Implement a calendar feature to track teacher attendance
OR
- Use a percentage and ask the teacher if you want to not grade for that day.
"""

# List to store lines from the CSV file
lines = []

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
x = 0

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
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Unix/Linux

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

with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)  # Skip header row
    
    for row in read:
        x += 1  # Increment line index
        lines.append(row)  # Append the row to lines
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        current_date = current_line[0][:-8]  # Extract date from current line
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index
        if user not in all_users: # Check if the user is unique
            all_users.append(user)
        if current_date not in all_days:
            all_days.append(current_date)
    x=-1
    today_users = []
    for row in read:
        x += 1  # Increment line index
        lines.append(row)  # Append the row to lines
        current_line = lines[x]
        user = new_email(current_line[1])  # Extract and clean email
        current_date = str(current_line[0][:-8])  # Extract date from current line
        color = row[2]  # Extract the color associated with the user
        class_number = int(color_to_number(color))  # Convert color to index
        prit("THIS IS THE THING:")
        print(str(checking_date.keys()[-1]))
        if str(checking_date.keys()[-1]) != current_date:
            checking_date[current_date] = None
            if int(all_users/2) >= today_users:
                sus_days[date] = int(today_users/int(all_users/2)*100)
            today_users = []
            # checking_sus_days = False
            today_users.append(user)
        else:
            today_users.append(user)



x = -1


# while True:
    # clear_console()
    #days = input(GREEN+"Benvenuto! Quanti giorni di 'Fai adesso' stai correggendo?\n\n--> "+PURPLE) 
    # days = str(len(all_days))

    # if days.isnumeric():
        # break
s

# Read the CSV file with form responses
with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
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
        for j in range(3, 8):  # Columns 3 to 7 are question responses
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
        
        # Update grades for the user
        if user in grades[color_to_number(color)]:  # If user already exists
            grades[color_to_number(color)][user] += i  # Increment points
        else:  # New user
            grades[color_to_number(color)][user] = i  # Set points
        
        # Update the most recent date for this user
        most_recent_user_date[user] = current_date
        names[user] = current_line[8]  # Store the user's name

# The following section is commented out but appears to be duplicate code
# for processing a different CSV file.


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
              " -- " + str(percentage) + "\n")