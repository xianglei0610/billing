# -*- coding: utf-8 -*-
import json
import datetime
import random
from hashlib import md5

from ooredis import String, Dict
import requests

import ams
from log_set import logger
import config
 
def get_user_oo(bid, uid):
    key = 'user:%s:%s'%(bid,uid)
    return Dict(key)

def get_display_status(bid, uid):
    m_oo = get_user_oo(bid, uid)
    try:
        m_val = m_oo["display_status"]
        if str(m_val)=='0':
            return False
        else:
            return True
    except:
        return True

def check_fn(bid, uid, number):
    m_oo = get_user_oo(bid, uid)
    try:
        m_val = m_oo["fn"]
        logger.info('get_fn_number_from_redis %s return %s '%( str( (bid, uid) ),m_val) )
        if m_val and m_val==number:
            return True
        else:
            return False
    except:
        return False

def get_phone_from_uid(brandid, uid):
    res = ams.getInfo(brandid, 'kc', uid)
    return res[2],res[4]

def get_uid_from_yid(brandid,yid):
    key = 'cloud:%s:%s'%(brandid, yid)
    ro = Dict(key)
    ret = ro['uid']
    logger.info(u'get_uid_from_yid( %s ) from Redis, return %s '%(  str( (brandid,yid) ),  ret) )
    try:
        ret = long(ret)
    except:
        raise Exception(u'fail to get uid from Redis')
    return ret


def getRand():
    n = datetime.datetime.now().strftime("%H%M%S")
    m = str(random.randint(1000, 9999))
    return n + m

def get_sign():
    macdate = datetime.datetime.now().strftime("%Y%m%d")
    macrand = getRand()
    macip = config.AMS_CONFIG.get('MAC_IP')
    key = config.AMS_CONFIG.get('MAC_KEY')
    sign = md5(macip + macdate + macrand + key).hexdigest()
    m_dict = {"macip":macip,
               "macdate":macdate,
               "macrand":macrand,
               "sign": sign}
    return m_dict

def  do_calllog_notify(content):
    content = json.dumps(content)
    payload = {
                'cat': 'billing_zh_calllog',
                'content': content,
               }
    payload.update( get_sign() )
    url = config.CIRCULATE_URL + "/circulate/transmit"
    r = requests.get(url, params=payload)
    if  r.status_code == 200:
        pass
#        res =  json.loads(r.text)
#        if res.has_key("result") and str(res["result"])==str(0):
#            return res["data"]["goods_type"]
#        else:
#            raise Exception(u'fail to do_calllog_notify %s return: %s'%(  content, r.text) )
    else:
        raise Exception(u'fail to do_calllog_notify %s return: %s'%(  content, r.text) )
    return 0

def get_inviter(uid, called):
    payload = {
                'uid': uid,
                'called': called,
               }
    url = 'http://weixin.weishuo.cn/api/get_inviter'
    r = requests.get(url, params=payload, timeout=6)
    if  r.status_code == 200:
        res =  json.loads(r.text)
        logger.info(u'to get_inviter %s return: %s'%(  str( (uid, called) ), r.text) )
        if res.has_key("code") and str(res["code"])==str(0):
            return False
        else:
            raise True
    else:
        logger.info(u'fail to get_inviter %s return: %s'%(  str( (uid, called) ), r.text) )
        raise Exception(u'fail to get_inviter %s return: %s'%(  str( (uid, called) ), r.text) )