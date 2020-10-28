#!/bin/bash

ps auxw | grep diag | grep -v grep > /dev/null

if [ $? != 0 ]
then
    echo "[Reboot] restarting the diag service at $(date)" >> /home/satyol/onrun/onrun_status.log

	cd /home/satyol/cambot
	python3 diag_service.py -c config/config.json &
fi

ps auxw | grep human_detect | grep -v grep > /dev/null

if [ $? != 0 ]
then
    echo "[Reboot] restarting the human detect service at $(date)" >> /home/satyol/onrun/onrun_status.log
    
    cd /home/satyol/cambot/
    python3 human_detect.cpython-37.pyc -c config/config.json &
fi
