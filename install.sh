# This file must be run as root to install the servic file in the correct location!

pip install -r requirements.txt

path_param=$1
delay_param=$2

chmod a+x rpi_slideshow.py
thisdir=`pwd`
cat rpislideshow.service.template \
| sed -e "s#EXEC_START_PATH#$thisdir/rpi_slideshow.py#" \
| sed -e "s#PATH#$path_param#" \
| sed -e "s#DELAY#$delay_param#" \
| sed -e "s#USER#$SUDO_USER#" > rpislideshow.service

systemctl enable $thisdir/rpislideshow.service
