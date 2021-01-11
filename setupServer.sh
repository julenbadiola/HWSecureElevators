#!/bin/bash
#Grove dependencies
curl -sL https://github.com/Seeed-Studio/grove.py/raw/master/install.sh | sudo bash -s -

#Dependencies for voice assistant
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
wget http://ftp.us.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
sudo apt-get install -f ./libttspico0_1.0+git20130326-9_armhf.deb ./libttspico-utils_1.0+git20130326-9_armhf.deb
rm -f *.deb

#Dependencies for voice recognition
sudo apt-get install -y flac alsa-tools alsa-utils libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test libilmbase-dev libopenexr-dev libgstreamer1.0-dev libavcodec-dev libavformat-dev libswscale-dev libwebp-dev

#Install required python packages
pip3 install -r requirements.txt