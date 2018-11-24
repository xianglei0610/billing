#!/usr/local/bin/python evn
# -*- coding: utf-8 -*-

import logging
from mlogging import TimedRotatingFileHandler_MP
import os

logger = logging.getLogger('billing_server')

options_set = {
               'logfile': './logs/run.log',
               'port': '8123',
               'backupCount': 100
               }

def configLog(options=options_set):
    u'''日志文件配置'''
    filename = "%s_%s" % (options.logfile, options.port)
    
    log_path = os.path.dirname(filename)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)

    formatter = logging.Formatter("[%(asctime)-11s]: %(module)s %(levelname)s %(message)s", '%d %H:%M:%S')
    handler = TimedRotatingFileHandler_MP(filename, when='midnight', backupCount=options.backupCount)
#    handler_email = logging.handlers.SMTPHandler(
#                config.MAIL_SERVER,
#                config.FROMADDR,
#                config.TOADDR,
#                config.SUBJECT,
#                config.CREDENTIALS
#    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
#    handler_email.setLevel(logging.ERROR)
    logging.getLogger('').addHandler(handler)
    #logging.getLogger('').addHandler(handler_email)
    logging.getLogger('').setLevel(logging.INFO)