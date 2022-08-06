import os
import sys
import git
import subprocess

repo = git.Repo("./")

def updateCode():
    currentVersion = getCurrentVersion()[0]
    ret = repo.remotes.origin.pull()
    try:
        repo.remotes.origin.pull()
        if getCurrentVersion()[0] == currentVersion:
            return "No changes"
        else:
            return "Updated"
    except:
        return "Network unreachable"

def getCurrentVersion():
    return str(repo.tags[-1]), str(repo.tags[-1].commit.message.replace("\n", " "))

def updateModules():
    ret = pipInstall("GitPython luma.oled flask flask_sqlalchemy")
    if ret == "Success":
        realCSSRepo = git.Repo("./static/RealCSS")
        try:
            realCSSRepo.remotes.origin.pull()
            return "Success"
        except:
            return "Network unreachable"
    elif ret == "Network unreachable":
        return "Network unreachable"

def pipInstall(module):
    proc = subprocess.Popen("sudo pip3 install --timeout 1000 " + module, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        #print(proc.stdout.readline())
        pass
    commandResult = proc.wait()
    if commandResult == 0:
        return "Success"
    else:
        return "Network unreachable"

if __name__ == "__main__":
    currentVersion = getCurrentVersion()
    print("Current Version: " + currentVersion[0])
    print("Description:     " + currentVersion[1])
    print("Updating code...")
    ret = updateCode()
    if ret == "No changes":
        print("No updates available")
    elif ret == "Updated":
        print("Code updated")
        currentVersion = getCurrentVersion()
        print("Current Version: " + currentVersion[0])
        print("Description:     " + currentVersion[1])
        print("Updating modules, make sure your internet connection is stable...")
        _ret = updateModules()
        if _ret == "Success":
            print("Modules updated")
            print("Now, you can restart the device.")
        elif _ret == "Network unreachable":
            print("Network error, please retry now to avoid any corruption!")
    elif ret == "Network unreachable":
        print("Network error, try again later")
