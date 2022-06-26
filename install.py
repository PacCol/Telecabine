import os, git

os.system("sudo systemctl stop rsyslog")
os.system("sudo systemctl disable rsyslog")
os.system("sudo raspi-config nonint do_i2c 0")

os.system("sudo apt-get install python3-pip")
os.system("sudo pip3 install GitPython")
os.system("sudo pip3 install luma.oled")
os.system("sudo pip3 install flask")
os.system("sudo pip3 install flask_sqlalchemy")

repo = git.Repo("./static/RealCSS")
repo.remotes.origin.pull()
