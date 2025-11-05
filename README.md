# Overview

This repository contains 4 programs:
 - a epaper driver for  https://www.waveshare.com/product/displays/e-paper/epaper-1/10.2inch-e-paper-hat-g.htm
   - these are the epdconfig.py and epd10in2g.py files
 - A test program that generates an image and calls the driver to display it
  - a program to generate binary files of the images
  - a web page used to control which message file to display
    - this is used in conjunction with an ESP32 running code from this repository: https://github.com/manningt/micropython-epd10

## epdconfig & epd10in2g.py
These were copied from waveshare's wiki and somewhat simplified: https://www.waveshare.com/wiki/10.2inch_e-Paper_HAT_(G)_Manual#Raspberry_Pi

## epd_10in2g_test.py
This creates a PIL image and calls epd.display to write it to the e-paper.
It takes 21 secconds to update the display.

## make_screen_bin.py
Creates a binary file of the PIL image.  The resulting files (with the .bin suffix) are meant to be copied to the e-paper control device, which in this case is an ESP, which can be battery powered.  There is code duplication between the _test.py program and the make_screen.py program; the duplicate code generates the Open/Closed messages.  Ideally this code would be moved to a seperate python file.

## Install FTP server
```
sudo apt install vsftpd
sudo systemctl enable vsftpd
```
No additional configuratution is necessary.  If you need to edit the ftp configuration, it is at /etc/vsftpd.conf.
The default ftp log is at /var/log/vsftpd.log.  If using a firewall, e.g. ufw, the access to the ftp port (21) should be allowed.

## webserver (app.py)
This flask based server displays a single page with buttons to select a message to display on the web page.
When a button is pushed, it deletes directories in ~/epaper that start with an m, and creates a new directory named 'mN' where N is the message number.  The epaper control device (the ESP) wakes up periodically and using FTP to check which 'mN' directory exists.  The epaper control device will change the display if the 'mN' directory has been changed.

Note: the 'routes.py' file is no longer used - its functions were migrated to app.py and simplified.

## monitor_esp
This script will be run as a service (run continually).  It is used to change the deep_sleep duration of the ESP in order to conserve battery energy.  When the Museum is open (12 to 3), the duration will be short (5 minutes); otherwise it will be long (4 hours or longer).  When the ESP wakes up, it will use FTP to check which 'tN' directory exists, where N is the deep sleep duration.  The script checks that the ESP is logging into the FTP server by looking at the tail of ```/var/log/vsftpd.log```


## TODO:
 - make a .service file to start app.py on boot.
 - make a .service file to start monitor_esp.py
 - finish coding monitor_esp.py (changing the times based on the day of the week)