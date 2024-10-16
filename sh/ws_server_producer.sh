#!/usr/bin/env bash

# set up timezone: Asia/Taipei
# sudo timedatectl set-timezone Asia/Taipei

# remember to restart cron service after time modification
# sudo /etc/init.d/cron restart

# application folder path
APP_HOME=$(dirname $(dirname $(readlink -f $0)))
echo ${APP_HOME}

# activate virtual environment
cd ${APP_HOME}
source .venv/bin/activate

# install required modules
pip3 install -r requirements.txt

# run application
pid=$(ps -ef | grep python | grep ws_server_producer | grep -v grep | awk '{print $2}')
echo $pid
kill -9 $pid
nohup python3 src/run_ws_server_producer.py >> log/run_ws_server_producer.log 2>&1 &

