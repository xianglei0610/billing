#!/usr/local/bin/python evn
# -*- coding: utf-8 -*-
import datetime
import json

from rq.redis import DefaultQueue as q

import rpc_call
import dao
import func
import config
from log_set import logger



def deal_called(content):
    #  参数获取
    logger.info(u'deal_called( %s )'%str(content) )
    
    callertype = content.get('callertype')  # 0：client帐号，1：普通电话
    caller = content.get('caller')
    callid = content.get('callid')
    calledtype = content.get('calledtype')
    
    appid = content.get('appid')
    calltype = content.get('calltype') # 0：直拨，1：免费，2：回拨
    yid = content.get('caller')
    called = content.get('called')
    
    starttime = content.get('starttime')
    stoptime = content.get('stoptime')
    length = content.get('length')
    
    userdata = content.get('userData','')
    if userdata:
        userdata = func.parse_data(userdata)
    else:
        userdata = {}
        
    buss_type = 1
    nickname = ''
    calleduid = ''  # 被叫uid
    if userdata.has_key("data"):
        m_data = userdata["data"]
        if m_data.has_key("buss_type"):
            buss_type = int(m_data["buss_type"])
        if m_data.has_key("nickname"):
            nickname = func.uncode_pwd(m_data["nickname"])
        if m_data.has_key("calleduid"):
            calleduid = m_data["calleduid"]
        
    bid = config.APPID_TO_BID[appid]
    uid = rpc_call.get_uid_from_yid(bid, yid)
    if not calleduid and str(calltype)=='1':
        calleduid = rpc_call.get_uid_from_yid(bid, called)

    number = called
    start_time = datetime.datetime.strptime(starttime,"%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(stoptime,"%Y-%m-%d %H:%M:%S")
    call_time = int(length)
    call_long = call_time
    # 获取计费时间
    call_unit = call_time / 60
    if call_time % 60>0:
        call_unit = call_unit + 1
    
    ############ 扣费 ############
    transaction_call_long_flag = False #只需要扣除套餐中的一部分计费时间
    transaction_cur_long_flag = False #要扣除套餐所有时间
    transaction_deduct_balance_flag = False #要扣除账户余额
    
    pkg_call_time = 0   #扣除套餐的时间
    billing_time = 0    #扣除账户余额的时间
    # 获取费率
    m_feerate,fee_type = func.get_feerate(bid, uid, number, calltype, userdata)
    if str(m_feerate)!='0':
        
        # 获取当前套餐可用时间
        cur_long = 0
        if number[:2] in config.NATIONAL_PREFIX or buss_type==3: #国际号码或陪聊号只能扣账户余额
            cur_long = 0
        else:
            if not config.TIME_PACKAGE_FLAG:
                cur_long = func.get_cur_long_total(bid, uid)/2
                
        # 得到扣除套餐的时间和扣除账户余额的时间 pkg_call_time, billing_time
        deduct_balance_val = 0
        if cur_long>=call_long:
            transaction_call_long_flag = True
            pkg_call_time = call_long
        else:
            if cur_long>0:
                transaction_cur_long_flag = True
                pkg_call_time = cur_long
    
            m_diff = call_long - cur_long
            m_unit = m_diff/60
            if m_diff % 60>0:
                m_unit = m_unit + 1
            deduct_balance_val = m_unit * m_feerate
            transaction_deduct_balance_flag = True
            billing_time = m_diff

    ############# 写入话单 ############
    obj = dao.get_new_log()
    obj.session = call_time and 1 or 0
    obj.brand = bid
    obj.from_number = uid
    obj.to_number = calleduid or number
    
    obj.start_time = start_time
    obj.end_time = end_time
    obj.call_time = call_time
    
    obj.pkg_call_time = pkg_call_time
    obj.billing_time = billing_time
    
    obj.field_rate = m_feerate
    obj.field_units = call_unit
    obj.field_fee = m_feerate*call_unit
    
    obj.call_year = 0
    obj.call_month = 0
    
    obj.call_type = calltype
    obj.field = buss_type
    obj.long_name = nickname
    
    ############# 执行事务 ###############
    with dao.database.transaction():
        if transaction_call_long_flag:
            logger.info(u'deduct_cur_packages %s'%str( (bid, uid, call_long) ) )
            ret = dao.deduct_cur_packages(bid, uid, call_long*2)
            if ret != 1:
                logger.error(u'fail to deduct_cur_packages %s'%str( (bid, uid, call_long) ) )
                raise Exception(u'扣减套餐失败, 上下文: %s'%content)
        if transaction_cur_long_flag:
            logger.info(u'deduct_cur_packages %s'%str( (bid, uid, cur_long) ) )
            ret = dao.deduct_cur_packages(bid, uid, cur_long*2)
            if ret != 1:
                logger.info(u'fail to deduct_cur_packages %s'%str( (bid, uid, cur_long) ) )
                raise Exception(u'扣减套餐失败, 上下文: %s'%content)
        if transaction_deduct_balance_flag:
            logger.info(u'deduct_balance %s'%str( (bid, uid, deduct_balance_val) ) )
            ret = func.deduct_balance(bid, uid, deduct_balance_val)
            if ret != 1:
                logger.info(u'fail to deduct_balance %s'%str( (bid, uid, deduct_balance_val) ) )
                raise Exception(u'扣减账户失败, 上下文: %s'%content)
            
        logger.info(u'add_call_log %s'%str( (bid, uid, obj.field_rate, obj.field_units, obj.field_fee) ) )
        ret = dao.add_call_log(obj)
        if ret != 1:
            logger.info(u'fail to add_call_log %s'%str( (bid, uid, obj.field_rate, obj.field_units, obj.field_fee) ) )
            raise Exception(u'写入话单失败, 上下文: %s'%content)
        #消息通知
        rpc_call.do_calllog_notify( {
                                     'bid': bid, 
                                     'uid': uid, 
                                     'calltype': calltype,     
                                     'to_number': number,
                                     'calleduid': calleduid,
                                     'call_time': call_time,
                                     'start_time': starttime,
                                     'end_time': stoptime,
                                     'nickname': nickname,
                                     'fee': m_feerate,
                                     'buss_type': buss_type
                                    })
    
    ############# 更新统计 #############
    ret = dao.update_call_info(bid, uid, start_time, call_long, fee_type)
    
    i_seconds = 0 # 国内通话秒数
    i_acc_seconds = 0 # 国内通话秒数(60的倍数)
    o_seconds = 0 # 国外通话秒数
    o_acc_seconds = 0 # 国外通话秒数(60的倍数)
    if not number[:2] in config.NATIONAL_PREFIX:
        i_seconds = call_time
        i_acc_seconds = call_unit*60
    else:
        o_seconds = call_time
        o_acc_seconds = call_unit*60
    ret = dao.update_call_stat(bid, uid, i_seconds, o_seconds, i_acc_seconds, o_acc_seconds)
    
def deal_called_async(content):
    result = q.enqueue(deal_called,content)
    return result
