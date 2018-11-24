#!/usr/local/bin/python evn
# -*- coding: utf-8 -*-

from mole import run

################### 异步任务队列初始化 ##############
from models import database
from rq import setup_db
setup_db(database)

###################加载 rq_dashboard ################
import rq_dashboard

if __name__  == "__main__":
    run(host='0.0.0.0', port=8124)