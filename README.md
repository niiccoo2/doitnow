## Do Now Autograder

This project was made to help with grading over 1,000 assignments every month.

![Photo showing the program asking if you wat to skip a day.](./Readme%20Assets/Screenshot%202025-01-08%2010.57.12%20AM.png)

![Photo showing final grade of test file.](./Readme%20Assets/Screenshot%202025-01-08%2010.57.33%20AM.png)

## Features:

1. Uses .csv file from google form.
2. Does not grade submissions on weekends. (Using datetime)
3. Only grades one submison per day per user.
4. If more than 50% of people don't respond one day it will ask if you don't want to grade that day.
5. If someone looks like they picked the wrong class one time program will move them.

## If things are not working right or don't look right:
- Check lines 291 and 292. the end of the range for line 199 should be question amount+4 but it may not be so also check that.