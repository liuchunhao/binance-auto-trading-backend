#!/usr/bin/env bash

APP_HOME=$(dirname $(dirname $(readlink -f $0)))
echo ${APP_HOME}

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
