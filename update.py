import os
import urllib.request
import git

repo = git.Repo("./")

def updateCode():
    if isConnected():
        ret = repo.remotes.origin.pull()
        print(ret[0].flags)
        if ret[0].flags == 4:
            return "No changes"
        else:
            return "Updated"
    else:
        return "Network unreachable"

def updateModules():
    if isConnected():
        os.system("sudo apt-get install python3-pip")
        os.system("sudo pip3 install GitPython")
        os.system("sudo pip3 install luma.oled")
        os.system("sudo pip3 install flask")
        os.system("sudo pip3 install flask_sqlalchemy")
        repo = git.Repo("./static/RealCSS")
        repo.remotes.origin.pull()
        return "Updated"
    else:
        return "Network unreachable"

def isConnected(host='http://github.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return True

if __name__ == "__main__":
    print(updateCode())
    #print(updateModules())
