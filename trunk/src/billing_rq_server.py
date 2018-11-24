#!/usr/local/bin/python evn
# -*- coding: utf-8 -*-

################### 异步任务队列初始化 ##############
from models import database
from rq import setup_db
setup_db(database)
    
################### 建立redis连接 ##################
import config
from ooredis import connect
connect(host=config.USER_REDIS_CONF["HOST"], port=int(config.USER_REDIS_CONF["PORT"]), password=config.USER_REDIS_CONF["PASSWORD"])
#################### 日志初始化 ###################
from log_set import configLog

class options_set():
    logfile = './logs/rqworker_server.log'
    port = 0
    backupCount = 50
    
configLog(options_set)
##################################################

if __name__  == "__main__":
    from rq.scripts.rqworker import main
    main()

