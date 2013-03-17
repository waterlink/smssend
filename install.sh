#!/bin/bash


sudo apt-get install libjpeg8 libpng12-0 libfreetype6 zlib1g

sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
sudo ln -s /usr/lib/i386-linux-gnu/libpng.so /usr/lib/libpng.so
sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/libz.so
sudo ln -s /usr/lib/i386-linux-gnu/libfreetype.so /usr/lib/libfreetype.so

virtualenv .sms
source .sms/bin/activate
pip install -r requirements.txt
