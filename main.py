# https://developers.google.com/forms/api/reference/rest/v1/forms.responses
import csv
import re
import os
import time
import math
lines=[]
grades={}
x=-1

BLACK  = "\033[30m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
PURPLE = "\033[35m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"
RESET  = "\033[0m"

def new_email(email):
    email = re.sub('[!@#$.]', '', email)
    email = ''.join(email.split())
    email = email[:-16]
    return email
with open('Fai Adesso - Form Responses 1.csv', newline='') as csvfile:
    read = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in read:
        x=x+1
        lines.append(row)
        current_line=lines[x]
        user = new_email(current_line[1])
        if not user or len(user) == 0:
            continue  # Skip processing if the email is invalid or empty

        #print(row)
        #print(user)
        i=0
        if row[2] != '':
            i=i+1
        if row[3] != '':
            i=i+1
        if row[4] != '':
            i=i+1
        if row[5] != '':
            i=i+1
        if row[6] != '':
            i=i+1
        if user in grades: # If user is already in the dict
            grades[user] = grades[user]+i
        else: # If user is new
            grades[user] = i

while True:
    os.system('clear')
    days = input(GREEN+"Benvenuto! Quanti giorni di 'Fai adesso' stai correggendo?\n\n--> "+PURPLE)

    if days.isnumeric():
        break
    os.system('clear')
    print(RED+"Enter a number.")
    time.sleep(3)

i=1
print(GREEN)
for i in range(len(grades)):
    key_at_position = list(grades.keys())[i]
    
    # Calculate percentage out of 100 and always round up
    percentage = math.ceil((grades[key_at_position] / 5 / int(days)) * 100)

    print(key_at_position + PURPLE + " --> " + GREEN + str(percentage) + "/ 100")

