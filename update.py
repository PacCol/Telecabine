import os
import urllib.request
import git

def update():
    if isConnected():
        print("UPDATING")
        os.system("git pull origin master")
        os.system("bash install.sh")
        print("UPDATED")
    else:
        print("no network")
        return "Network unreachable"

def isConnected(host='http://github.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

if __name__ == "__main__":
    update()
