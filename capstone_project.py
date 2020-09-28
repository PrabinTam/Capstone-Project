import psutil
import os
import subprocess
import requests
import time


#This iterates over all the process and gets the attributes [path of the processes] of our choice in dictonary format
# Then writes it in a file called hash_path.txt.
def get_list_of_process():
    with open("hash_path.txt", "w") as f:
        for proc in psutil.process_iter():      #loops through all the processes
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'exe'])
            except psutil.NoSuchProcess:
                pass
            else:
                if pinfo["exe"] == None or "\\" not in pinfo["exe"]:
                    pass
                else:
                    f.write(pinfo["exe"] + "\n")        # writes the path into the file

#runs the powersehll script which will take the hash of the processes and writes into a file
def run_powershell():
    try:
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Unrestricted", "./calculate_hash.ps1", ">", "hash_file.txt"], capture_output=True)
    except:
        pass
    # deletes the file with path becuase new file is created with the path and the hash in it.
    os.remove("hash_path.txt")
 
#reading the hash from the file and parsing it to send it to virustotal function to get the result
def hash_file_read():
    if os.path.isfile("result.txt"):
        os.remove("result.txt")
    with open("hash_file.txt", "r", encoding="utf-16") as f:
        count = 0
        for line in f:
            if "\\" in line:
                count+= 1
                line = line.strip()
                line = line.split("  ")
                hash = line[-1]         # Hash digest
                path = line[0]          # path of the file
                if count == 4:
                    time.sleep(61)      # sleep for 1 minute
                    count = 0
                result_virustotal(hash, path)       # sends the hash to the virustotal for result
            else:
                continue

# This function will take the hash and runs it against its data base with several AV
# engnies and tell us if it is malicious or not
def result_virustotal(hash, path):
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    params = {'apikey': '4fd8c58a3a45e86e738842a11821f34a0478c974be0cc773b6a458f4f350fb06', 'resource': hash}
    response = requests.get(url, params)
    response = response.json()

    with open("result.txt", "a+") as f:
        if response["response_code"] == 1:      # value 1 if the has provided was in the database
            if response["positives"] == 0:      # value 0 means that not a single AV found the hash malicious
                f.write("%s in this path %s is not malicious \n" % (hash, path))
                return
            else:
                f.write("---------------------------------")
                f.write("%s in this path %s is malicious\n" % (hash, path))
                f.write("%s many AV engies out of %s found it to be malicious"% (response["positives"], response["total"]))
                f.write("---------------------------------")
        else:
            f.write("Provided hash %s could not be found in the database for path %s"%(hash, path))

if __name__ == '__main__':
    get_list_of_process()
    run_powershell()
    hash_file_read()