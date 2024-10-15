import csv
import re
import os
import time
import math

"""
Thing to do:
Add better names
only 3 questions for 6th grade Giallo/Viola
"""

lines=[]
#grades={"Rosso": {}, "Arancione": {}, "Giallo": {}, "Verde": {}, "Blu": {}, "Viola": {}} # Tried 
grades = [{},{},{},{},{},{}]
colors = ["Rosso", "Arancione", "Giallo", "Verde", "Blu", "Viola"]
names = {}
most_recent_user_date = {}

x =- 1

BLACK  = "\033[30m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
PURPLE = "\033[35m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"
RESET  = "\033[0m"

def color_to_number(color):
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
    email = re.sub('@watertown.k12.ma.us', '', email)
    return email
    
with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(read)
    for row in read:
        x=x+1
        lines.append(row)
        current_line=lines[x]
        user = new_email(current_line[1])
        if user not in most_recent_user_date:
            most_recent_user_date[user]=None
        current_date=current_line[0][:-8]
        if not user or len(user) == 0:
            continue  # Skip processing if the email is invalid or empty
        color=row[2]
        class_number=int(color_to_number(color))
        i=0
        if row[3] != '':
            i=i+1
        if row[4] != '':
            i=i+1
        if row[5] != '':
            i=i+1
        if row[6] != '':
            i=i+1
        if row[7] != '':
            i=i+1
        if most_recent_user_date[user] == current_date:
            continue
        if user in grades[color_to_number(color)]: # If user is already in the dict
            grades[color_to_number(color)][user] = grades[color_to_number(color)][user]+i
        else: # If user is new
            grades[color_to_number(color)][user] = i
        most_recent_user_date[user] = current_date
        names[user] = current_line[8]
# with open('Fai Adesso - Form Responses 6th.csv', newline='') as csvfile:
#     read = csv.reader(csvfile, delimiter=',', quotechar='"')
#     next(read)
#     for row in read:
#         x=x+1
#         lines.append(row)
#         current_line=lines[x]
#         user = new_email(current_line[1])
#         if user not in most_recent_user_date:
#             most_recent_user_date[user]=None
#         current_date=current_line[0][:-8]
#         if not user or len(user) == 0:
#             continue  # Skip processing if the email is invalid or empty
#         color=row[2]
#         class_number=int(color_to_number(color))
#         i=0
#         if row[3] != '':
#             i=i+1
#         if row[4] != '':
#             i=i+1
#         if row[5] != '':
#             i=i+1
#         if row[6] != '':
#             i=i+1
#         if row[7] != '':
#             i=i+1
#         if most_recent_user_date[user] == current_date:
#             continue
#         if user in grades[color_to_number(color)]: # If user is already in the dict
#             grades[color_to_number(color)][user] = grades[color_to_number(color)][user]+i
#         else: # If user is new
#             grades[color_to_number(color)][user] = i
#         most_recent_user_date[user] = current_date


while True:
    os.system('clear')
    days = input(GREEN+"Benvenuto! Quanti giorni di 'Fai adesso' stai correggendo?\n\n--> "+PURPLE)

    if days.isnumeric():
        break
    os.system('clear')
    print(RED+"Enter a number.")
    time.sleep(3)

# Display grades
while True:
    os.system('clear')  # Clear the terminal
    print(GREEN)
    for y in range(len(grades)):
        current_color = colors[y]  # This is just for display
        print(PURPLE + current_color + ":\n"+GREEN)
        for i, key_at_position in enumerate(grades[y].keys()):  # Use 'y' to access grades, not 'current_color'
            percentage = math.ceil(grades[y][key_at_position] / 5 / int(days) * 100)
            print(names[key_at_position] + " / " + key_at_position + PURPLE + " --> " + GREEN + str(percentage) + "/100\n")
    
    break  # Exit the loop after printing once

