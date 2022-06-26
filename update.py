import os
import urllib.request
import git

repo = git.Repo("./")

def update():
    if isConnected():
        print("UPDATING")
        ret = repo.remotes.origin.pull()
        if ret[0].flags == 4:
            print("No changes")
        else:
            print("Updated")
        #os.system("bash install.sh")
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
