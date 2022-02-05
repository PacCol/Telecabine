sudo systemctl stop rsyslog
sudo systemctl disable rsyslog
sudo raspi-config nonint do_i2c 0
cd static
rm -rf RealCSS
git clone https://github.com/PacCol/RealCSS.git
sudo pip3 install luma.oled
