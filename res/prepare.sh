#!/bin/sh
mkdir -p /home/$2/log
chown -R 1913:1913 /home/$2/log;chmod -R 775 /$2/dlna/log
echo "friendly_name=$1" >> /var/$2/res/minidlna.conf
