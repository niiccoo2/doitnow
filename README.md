## Do Now Autograder

This project was made to help with grading over 1,000 assignments every month. (Last updated on 01-08-2025)

![Photo showing the program asking if you wat to skip a day.](./Readme%20Assets/Screenshot%202025-01-08%2010.57.12%20AM.png)

![Photo showing final grade of test file.](./Readme%20Assets/Screenshot%202025-01-08%2010.57.33%20AM.png)

## Features:

- Uses .csv file from google form.
- Does not grade submissions on weekends. (Using datetime)
- Only grades the first submison per day per user. 
- If more than 50% of people don't respond one day it will ask if you want to skip grading for that day.
- If a user looks like they picked the wrong class the program will correct it (It uses probibility with all responses so it may be wrong)
- Reads the csv header and uses that to learn how many questions there are.

## TODO:

- GUI ([Easygui?](https://easygui.sourceforge.net/))
- Read class names dynamically
- Use [PyInstaller](https://pyinstaller.org/en/stable/) to make a mac install file
- Test on Mac
