#!/bin/bash

server="billing_server.py"

if [ -f "$server" ]; then
billing_server="billing_server.py"
rqworker_server="billing_rq_server.py"
else
billing_server="billing_server.pyc"
rqworker_server="billing_rq_server.pyc"
fi 

ps aux|grep $billing_server | grep -v grep|awk '{print $2}'|xargs kill -9

ps aux|grep $rqworker_server | grep -v grep|awk '{print $2}'|xargs kill -9
ps aux|grep $rqworker_server | grep -v grep|awk '{print $2}'|xargs kill -9
if [ ! -d "logs" ]; then mkdir "logs"; fi;

nohup python $billing_server -p4611 -m >/dev/null &
nohup python $billing_server -p4612 >/dev/null &
nohup python $billing_server -p4613 >/dev/null &

nohup python $rqworker_server >/dev/null &

