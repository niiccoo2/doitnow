import csv
import re
import os
import time
import math
import datetime

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
current_line = []
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