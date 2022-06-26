sudo systemctl stop rsyslog
sudo systemctl disable rsyslog
sudo raspi-config nonint do_i2c 0
cd static
rm -rf RealCSS
git clone https://github.com/PacCol/RealCSS.git
sudo apt-get install python3-pip
sudo pip3 install luma.oled
sudo pip3 install flask
sudo pip3 install flask_sqlalchemy
sudo pip3 install python-git