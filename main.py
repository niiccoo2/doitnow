#####################################################################################
#  ____   ___ ___ _____ _   _  _____        __
# |  _ \ / _ \_ _|_   _| \ | |/ _ \ \      / /
# | | | | | | | |  | | |  \| | | | \ \ /\ / / 
# | |_| | |_| | |  | | | |\  | |_| |\ V  V /  
# |____/ \___/___| |_| |_| \_|\___/  \_/\_/   
#####################################################################################
#
# Change these values if the location of data changes in csv.
# 
# EXAMPLE: This means that in doitnow.csv, the order is date, email, name, class_color.
#
# date=0 # If you use google forms then date is almost always 0. 
# email=1
# class_color=3
# name=2
#
# EXAMPLE ^^^
#
# CHANGE THESE LINES:
date=0 
email=1
class_color=3
name=2
#
# DON'T change any lines below of you don't know what you are doing.
#####################################################################################

pickfile = 2 # 1 = test, 2 = 7/8, 3 = 6th

import csv
import re
import os
import time
import math
import datetime
import tkinter
from tkinter import filedialog


try:
    file_name = 'doitnow.csv'
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile, delimiter=',', quotechar='"')
        print("Using doitnow.csv")
except:
    print("Using pickfile.")
    if pickfile==1:
        file_name = 'Fai Adesso - Form Responses TEST.csv' # Test
    elif pickfile==2:
        file_name = "Fai Adesso - Aprile 7th - 8th (Responses) - Form Responses 1.csv" # 7/8
    else:
        file_name = "Fai Adesso - Aprile - 6th Grade (Responses) - Form Responses 1.csv" # 6th


# Initialize grades dictionary for each color group
grades = [{}, {}, {}, {}, {}, {}]
colors = ["rosso", "arancione", "giallo", "verde", "blu", "viola"]
names = {}  # To store names associated with users
most_recent_user_date = {}  # To track the last date each user submitted
sus_days = {}
all_users = []
all_days = []
excluded_days = []
corrected_users = []
classes = []
missedpoints = 0
lines = []
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
GRAY = "\033[90m"
RESET = "\033[0m"

def clear_console():
    # Clear the terminal screen based on the OS.
    # if os.name == 'nt':
    #     os.system('cls')  # Windows
    # else:
    #     os.system('clear')  # Unix/Linux
    print("FAKE CLEAR")


def color_to_number(color):
    color = color.lower()  # Ensure the color is in lower-case
    if color == "rosso":
        return 0
    elif color == "arancione":
        return 1
    elif color == "giallo":
        return 2
    elif color == "verde":
        return 3
    elif color == "blu":
        return 4
    elif color == "viola":
        return 5
    else:
        return -1


def new_email(email):
    # Clean up the email address by removing the domain.
    email = re.sub('@watertown.k12.ma.us', '', email)
    return email

# def findclass(user): # Old
#     for f in range(len(classes)):
#         if user in classes[f]:
#             return f
        
def findclass(user): # New
    for f in range(len(classes)):
        if user in classes[f]:
            return f
    # If user is not found, return a default value (or raise an error if needed)
    return -1  # Could raise an error or handle as needed


with open(file_name, newline='', encoding='utf-8') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in read:
        header=row
        break
    # next(read)  # Skip header row    
    for row in read:
        lines.append(row)  # Append the row to lines

question_amount=len(row)-4

for row in lines: # Adding users and days to all_users and all_days while skiping weekends
    user = new_email(row[email])  # Extract and clean email
    current_date = row[date].split(" ")[0]  # Extract date from current line
    color = row[class_color]  # Extract the color associated with the user
    class_number = int(color_to_number(color))  # Convert color to index
    # Convert date string to datetime object
    datetime_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
    week_number = datetime_obj.weekday()  # Get the weekday (Monday=0)
    
    # Skip weekends (Saturday=5, Sunday=6)
    if week_number == 5 or week_number == 6 or current_date in excluded_days:
        continue
    if user not in all_users: # Check if the user is unique
        all_users.append(user)
    if current_date not in all_days:
        all_days.append(current_date)

today_users = []
last_checked_date = ""  # Track the date to detect changes

for row in lines: # Adding users to sus_days
    user = new_email(row[email])  # Extract and clean email
    current_date = row[date].split(" ")[0] # Extract date from current line
    color = row[class_color]  # Extract the color associated with the user
    class_number = int(color_to_number(color))  # Convert color to index

    # If the date has changed, process the previous day and reset `today_users`
    if last_checked_date == "": # Will add the the begining of the loop after code works.
        last_checked_date = current_date
    if current_date != last_checked_date:
        # Check if the number of today's users is less than half of all users
        if len(today_users) / len(all_users) <= 0.5:
            sus_days[last_checked_date] = int(len(today_users) / len(all_users) * 100)
        # Reset `today_users` for the new day
        today_users = []  # Reset for the new day

    if user not in today_users:
        today_users.append(user)

    # Update the last_checked_date for the next iteration
    last_checked_date = current_date
    x += 1  # Increment line index

# Handle the last date after the loop ends
if last_checked_date and len(today_users) / len(all_users) <= 0.5:
    sus_days[last_checked_date] = int(len(today_users) / len(all_users) * 100)

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
        #print(day_key)
        #print(sus_days[day_key])
        print(f"{RED}{day_key}{GRAY} may be a day that there was no school, or the teacher was absent. Only {RED}{sus_days[day_key]}{GRAY} percent of people responded on this day.")
        override_sus_days = input("Do you want to include this day? (Y/n)\n" + RED).strip().lower()
        
        if override_sus_days in ["yes", "y", ""]:
            #print("Include")
            break  # Exit loop if the day is included
        elif override_sus_days in ["no", "n"]:
            excluded_days.append(day_key)  # Add day to excluded days
            days -= 1  # Adjust the total days
            #print("Exclude")
            break  # Exit loop after excluding day
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

for row in lines: # Read the CSV file with form responses
    user = new_email(row[email])  # Extract and clean email
    if user not in most_recent_user_date:
        most_recent_user_date[user] = None  # Initialize date tracking
    
    current_date = row[date].split(" ")[0]  # Extract date from current line
    
    if not user or len(user) == 0:
        continue  # Skip invalid or empty emails
    
    color = row[class_color]  # Extract the color associated with the user
    class_number = int(color_to_number(color))  # Convert color to index
    
    # Count non-empty responses for the user
    i = 0
    for j in range(4, len(header)):  # Columns 4 to 8 are question responses
        if row[j] != '' and row[j].lower() != "idk" and row[j].lower() != "i dont know" and row[j].lower() != "idk." and row[j].lower() != "i dont know." and row[j].lower() != "i don't know" and row[j].lower() != "i don't know.":
            i += 1
    
    # Convert date string to datetime object
    datetime_obj = datetime.datetime.strptime(current_date, '%m/%d/%Y')
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
    names[user] = row[name]  # Store the user's name
    x += 1  # Increment line index

    currentclass = row[class_color] # this finds the class
    if user not in corrected_users: # checks if the user is unique so far
        classes.append([user, 0, [currentclass]]) # adds them to a list of people with some info
        corrected_users.append(user) # makes them not count as unique later
    else:
        classes[findclass(user)][-1].append(currentclass) # adds their class to the data
    classes[findclass(user)][-1].sort() # sorts the data for later use

# classes = [["user", missedpoints, ["class", "class", ect]],[],[]]
corrected_users = []
z=0
for row in lines:
    currentclass = row[class_color]
    user = new_email(row[email])
    # if user == "tosceo708":
    #     print("\n")
    #     print(z)
    #     z=z+1
    #     print("\n")
    if user not in corrected_users:
        corrected_users.append(user)
        classes[findclass(user)][-1] = classes[findclass(user)][-1][int(len(classes[findclass(user)][-1])/2)]
        # print(classes)
    if currentclass != classes[findclass(user)][-1]:
        # Check if the user exists in the grades for the current class

        current_class_index = colors.index(currentclass.lower())  # Get the index for the current class
        if user not in grades[current_class_index]:
            grades[current_class_index][user] = 0  # Initialize the grade if not found

        # Now safely update the grade
        classes[findclass(user)][1] += grades[current_class_index][user]

        # Afterward, delete the user from the grades list to prevent duplication
        del grades[current_class_index][user]

        ###### OLD -- CLEAN UP ######
        # classes[findclass(user)][1] += grades[colors.index(currentclass)][user]
        # # print(findclass(user))
        # # exit()
        # del grades[colors.index(currentclass)][user]
        ###### ^^^^^^^^^^^^^^^ ######

#grades[colors.index(classes[findclass(all_users[i])][-1][color_to_number(classes[findclass(all_users[i])][-1][len(classes[findclass(all_users[i])][-1])/2])])][all_users[i]] += classes[findclass(all_users[i])][1]

# print(classes[findclass(all_users[0])][1])
# exit()
# for i in range(len(all_users)):
#     for l in range(len(colors)):
#         # print(classes[findclass(all_users[i])][-1])
#         # exit()
#         if classes[findclass(all_users[i])][-1] == colors[l].lower():
#             grades[color_to_number(colors[l].lower())][all_users[i]] += classes[findclass(all_users[i])][1]

for i in range(len(all_users)):
    final_class = classes[findclass(all_users[i])][-1]  # The user's final class as a string (e.g., "rosso")
    final_points = classes[findclass(all_users[i])][1]    # The aggregated points for that user
    for l in range(len(colors)):
        if final_class == colors[l].lower():
            color_index = color_to_number(colors[l].lower())
            # Initialize the user in the dictionary if not present
            if all_users[i] not in grades[color_index]:
                grades[color_index][all_users[i]] = 0
            grades[color_index][all_users[i]] += final_points


# Display grades
clear_console()
print(RED)
for y in range(len(grades)):
    current_color = colors[y].lower()  # For display purposes
    print(GRAY + current_color.title() + ":\n" + RED)
    for i, key_at_position in enumerate(grades[y].keys()):  # Access grades by index
        # Calculate percentage score
        #percentage = math.ceil(grades[y][key_at_position] / 5 / int(days) * 100)
        percentage = (int(grades[y][key_at_position]) / (int(days) * question_amount)) * 100
        print(names[key_at_position] + GRAY + " -- " + RED + key_at_position + GRAY + " --> " +
              RED + str(grades[y][key_at_position]) + "/" + str(int(days) * question_amount) + GRAY + 
              " -- " + RED + str(int(percentage)) + "%\n")

print(RESET)