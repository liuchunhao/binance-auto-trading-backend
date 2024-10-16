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
# pip3 install -r requirements.txt

# run application
python3 src/run_futures_account_status_notify.py

