#! /usr/bin/python3
import os
from capstone.capstone_project import result_virustotal
import subprocess
import getpass
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# This script wll detect any file that is created in the system.
# The root path of this is set to the user's profile rather than the C:\ drive itself.

# get the hash of the file
def hash_file_detection(path):
    hash = subprocess.run(["powershell.exe", "Get-Filehash", path, "-algorithm", "sha256", "|Format-List"], capture_output=True)
    hash = hash.stdout.decode().strip().replace(" ", "").replace("\r", "").split("\n")
    sha256 = hash[1].replace("Hash:", "")
    result_virustotal(sha256, path)

# Class that will decide what happens when a new file was detected
class Handler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(self, patterns="*", ignore_directories=False, case_sensitive=True)
    def on_created(self, event):
        path = event.src_path
        if "AppData" not in path:       # This is set so that temp/cache files are skipped for any program.
            hash_file_detection(path)

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
    initiate_watchdog()