# Do Now Autograder

This project was made to help with grading over 1,000 assignments every month.

# Features:

1. Uses .csv file from google form.
2. Does not grade submissions on weekends. (Using datetime)
3. Only grades one submison per day per user.
4. If more than 50% of people don't respond one day it will ask if you don't want to grade that day.
5. 

# This is the old print statement: 

```
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
        print(names[key_at_position] + " -- " + key_at_position + PURPLE + " --> " +
              GREEN + str(grades[y][key_at_position]) + "/" + str(int(days) * 5) + 
              " -- " + str(int(percentage)) + "%\n")
```