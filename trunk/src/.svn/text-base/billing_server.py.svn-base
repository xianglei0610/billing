#!/usr/local/bin/python evn
# -*- coding: utf-8 -*-
##################### 系统环境设置 #######################
def set_lib_path():
    import sys
    import os
    sys.path.append('./libs')
#set_lib_path() 

import config


def main(block=False):
    ################# 运行参数和日志的初始化 #################
    from optparse import OptionParser
    from log_set import configLog
    parser = OptionParser(usage="usage: python %prog [options] filename",version="Billing" )
    parser.add_option("-p", "--port",
                      action="store",
                      type="int",
                      dest="port",
                      default=8223,
                      help="Listen Port")
    parser.add_option("-f", "--logfile",
                      action="store",
                      type="string",
                      dest="logfile",
                      default='./logs/billing_server.log',
                      help="LogFile Path and Name. default=./logs/billing_server.log")
    parser.add_option("-n", "--backupCount",
                      action="store",
                      type="int",
                      dest="backupCount",
                      default=100,
                      help="LogFile BackUp Number")
    parser.add_option("-m", "--master",
                      action="store_true",
                      dest="master",
                      default=False,
                      help="master process")
    (options, args) = parser.parse_args()
    configLog(options)
    ################### 初始化数据库表 #################
#    from models import Call_Log,Call_Log_Next
#    from models import T_Callstat,T_Callstat_Next
#    Call_Log.create_table(True)
#    Call_Log_Next.create_table(True)
#    T_Callstat.create_table(True)
#    T_Callstat_Next.create_table(True)

    #################### 定时任务 #####################
    if options.master:
        import cron
        cron.main()
    ################### 建立redis连接 ##################
    from ooredis import connect
    connect(host=config.USER_REDIS_CONF["HOST"], port=int(config.USER_REDIS_CONF["PORT"]), password=config.USER_REDIS_CONF["PASSWORD"])
    ################### 异步任务队列初始化 ##############
    from models import database
    from rq import setup_db
    setup_db(database)
    #################### 加载模块 #####################
    import interface
    #################### 启动服务 #####################
    from mole import run
    from mole.mole import default_app
    app = default_app()
    if block:
        run(app=app, host='0.0.0.0', port=options.port, server='gevent')


if __name__  == "__main__":
    main(block=True)
