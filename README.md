# Mini-Antivirus

External Libraries used in this project so far:

    Watcdog
    psutil
    requests

This project is still ongoing project hence the files I have commited will undergo changes. 

Now, what does this project do?
    This project is writeen in python, which will act as a mini-antivirus
How is it a Mini-antivirus:

    First The script gets all the process running on the Windows OS and check if it is malicious or not by taking the hash of the process
    and running it against the virus total, using its API to determine if it is malicious. [Completed]
    
    The Second part of the script will run in the system in startup and detect if any file is added on the system. Once it detects that file has been added to the system , it will check if it is malicious or not using the same process as the first part of the project. [Completed]
    
    The third part of the script is going to go through all the files inlcuding the new ones that gets added, and checks if it contains personal informion such as
    Credit Card number and SSN and lets the users know about it. [Ongoing]
    
    Note: Just because it states that it is completed does not mean it is complted, it just means that it does what the description states but still needs some work to make it look better!
    
    
