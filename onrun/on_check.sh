#!/bin/bash

ps auxw | grep diag | grep -v grep > /dev/null

if [ $? != 0 ]
then
    echo "[Restart] starting the diag service at $(date) since its NOT running" >> /home/satyol/onrun/onrun_status.log

	cd /home/satyol/cambot
	python3 diag_service.py -c config/config.json &
fi

ps auxw | grep human | grep -v grep > /dev/null

if [ $? != 0 ]
then
    echo "[Restart] starting the human detection service at $(date) since its NOT running" >> /home/satyol/onrun/onrun_status.log

        cd /home/satyol/cambot
        python3 human_detect.cpython-37.pyc -c config/config.json &
fi
