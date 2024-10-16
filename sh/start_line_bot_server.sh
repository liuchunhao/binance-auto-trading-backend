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
pid=$(ps -ef | grep python | grep -v grep | grep line_bot_server | awk '{print $2}')
[ -z "$pid" ] || {
    echo "kill previous line_bot_server process: $pid"
    kill -9 $pid
}
nohup python3 src/run_line_bot_server.py >> log/line_bot_server.log 2>&1 &
pid=$(ps -ef | grep python | grep -v grep | grep line_bot_server | awk '{print $2}')
echo "line_bot_server process: $pid"

