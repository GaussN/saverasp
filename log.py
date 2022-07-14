import sys
import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

def successLog(log: str):
    date = datetime.datetime.now()  
    print(f'{Back.GREEN}{Fore.WHITE}{date} {log}')

def warningLog(log: str):
    date = datetime.datetime.now()    
    print(f'{Back.YELLOW}{Fore.WHITE}{date} {log}')
    
def errorLog(log: str):
    date = datetime.datetime.now()  
    print(f'{Back.RED}{Fore.WHITE}{date} {log}')

def log(log: str):
    date = datetime.datetime.now()  
    print(f'{Style.DIM}{date} {log}')
    
if __name__ == '__main__':
    successLog("success")
    warningLog("warning")
    errorLog("error")
    log("log")