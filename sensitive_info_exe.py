from capstone.file_detection_exe import initiate_watchdog
import os
import time

# The scritp here will go through all the files [txt, csv, docs and xls] in the system as long as
# And check if they contain any personal information. 


# This checks if the file has any potential credit card number.
def credit_card_check(path):
    credit_card = []
    with open("test.txt", "r") as f:
        for line in f:
            if any(map(str.isdigit, line)) == True:         # only if the line consists of a number
                line = line.strip()
                line = line.replace("\n", "").replace("  ", " ")
                line = line.split(" ")
                for digit in line:
                    if digit.digit():             # if all the strings are all num
                        if len(digit) == 15 or len(digit) == 16:    # if the string legth is equal to 15 or 16
                            credit_card.append(digit)
    return credit_card
    
def detect_sensitive_file(path):
    credit_card_check(path)

class Handler(PatternMatchingEventHandler):
    def __init__(self):
        patterns =[".txt", ".csv", ".doc", ".docs", ".xls", ".xlsx", ".ppt", ".pptx"]
        PatternMatchingEventHandler.__init__(self, patterns = patterns, ignore_directories=False, case_sensitive=True)
    def on_created(self, event):
        path = event.src_path
        if "AppData" not in path:
            detect_sensitive_file(path)


if __name__ == "__main__":
    initiate_watchdog()
