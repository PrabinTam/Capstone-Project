from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import time
import getpass

# The scritp here will go through all the files [txt, csv, docs and xls] in the system as long as
# And check if they contain any personal information.

# Function that will check if the potential credit card number is a valid credit card or not based on Lunh Algorith aka module 10.
def lunh_algorithm(credit_card_check):
    credit_card_sum = 0
    count = 1
    if len(credit_card_check) >= 1:
        for credits in credit_card_check:
            for nums in credits:
                count += 1
                if count % 2 == 0:              # every even place
                    num =  str(int(nums) * 2)
                    if len(num) > 1:
                        for i in num:
                            credit_card_sum += int(i)
                    else:
                        credit_card_sum += int(num)
                else:
                    credit_card_sum += int(nums)
            print(credit_card_sum)
            if credit_card_sum % 10 == 0:
                credit_card_sum = 0
                print("Valid credit card", credits)
            else:
                credit_card_sum = 0
                print("nope")

# This checks if the file has any potential credit card number.
def get_potential_credit_card(path):
    credit_card = []
    with open(path, "r") as f:
        for line in f:
            if any(map(str.isdigit, line)) == True:         # only if the line consists of a number
                line = line.strip()
                line = line.replace("\n", "")
                line = line.split()
                for digit in line:
                    if digit.isdigit():             # if all the strings are all num
                        if len(digit) >= 15 and len(digit) <= 19:    # if the string legth is equal to 15 or 16
                            credit_card.append(digit)
            else:
                continue
    return credit_card

# function that will check if there is a sensitive data or not
def detect_sensitive_file(path):
    credit_card = get_potential_credit_card(path)
    lunh_algorithm(credit_card)

# This will tell us how to handle once the new file has been detected.
class Handler(PatternMatchingEventHandler):
    def __init__(self):
        patterns =["*.txt", "*.csv", "*.doc", "*.docs", "*.xls", "*.xlsx"]           # detect file with only these extentions.
        PatternMatchingEventHandler.__init__(self, patterns = patterns, ignore_directories=False, case_sensitive=True)
    def on_created(self, event):
        path = event.src_path
        if "AppData" not in path:
            print(path)
            detect_sensitive_file(path)

# Initite file detection in the system
def initiate_watchdog():
    username = getpass.getuser()  # getting the usernam of the user
    path = r"C:\Users\%s" % username
    src_path = path
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    initiate_watchdog()             # detect hen a new file is added in the system with C:\ as the root path
