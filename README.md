# Telecabinee
A simple Raspberry Pi web server to control a lego detachable gondola

## Installation
Clone the repository as root.
```bash
cd /home/pi
sudo git clone https://github.com/PacCol/Telecabine.git
cd Telecabine
sudo python3 install.py
```

Now, we have to make sure that the server starts on startup.
```bash
sudo vi /etc/rc.local
```
We add two lines to the rc.local file...
```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

cd /home/pi/Telecabine/  # Go into the working directory
sudo python3 server.py   # Launch the web server

exit 0
```
