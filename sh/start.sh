#!/usr/bin/env bash

APP_HOME=$(dirname $(dirname $(readlink -f $0)))
echo ${APP_HOME}

cd ${APP_HOME}
source .venv/bin/activate

pip3 install -r requirements.txt

# stop all processes
apps=(
    "ws_server_producer"
    "line_bot_server"
)

for app in ${apps[@]}
do 
    pid=$(ps -ef | grep python | grep -v grep | grep ${app} | awk '{print $2}')
    [ -z "${pid}" ] || { 
        kill -9 $pid
        echo ${app}: PID=[$pid] killed
    }
done


# restart redis
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml up -d

# start all
nohup python3 src/run_ws_server_producer.py >> log/run_ws_server_producer.log 2>&1 &
nohup python3 src/run_line_bot_server.py    >> log/line_bot_server.log 2>&1 &

