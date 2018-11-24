# -*- coding: utf-8 -*-
import datetime
import os
import time
import json

from mole import route, request, response

import async
import rpc_call
import dao
import func
import config
from log_set import logger
from dao import dbop

@route('/api/precall_notify/', method=["GET","POST"])
@dbop
def precall_notify():
    content = func.get_context_data_dict(request)
    logger.info(u'precall_notify( %s )'%str(content) )
    
    callertype = content.get('callertype')  # 0：client帐号，1：普通电话
    caller = content.get('caller')
    calledtype = content.get('calledtype')
    
    appid = content.get('appid')
    calltype = content.get('calltype') # 0：直拨，1：免费，2：回拨
    yid = content.get('caller')
    called = content.get('called', '')
    userdata = content.get('userData','')
    
    if userdata:
        userdata = func.parse_data(userdata)
    else:
        userdata = {}
        
    buss_type = 1   #呼叫业务类型
    i_fee = None    #费率
    if userdata.has_key("data"):
        m_data = userdata["data"]
        if m_data.has_key("raw"):
            #Rest回拨直接返回上次鉴权数据
            rawdata =  m_data["raw"]
            return func.response_data_xml(request, rawdata)
        if m_data.has_key("buss_type"):
            buss_type = int(m_data["buss_type"])
        if m_data.has_key("fee"):
            i_fee = int(m_data["fee"])
    
    bid = config.APPID_TO_BID[appid]
    uid = rpc_call.get_uid_from_yid(bid, yid)
    
    number = called
    
    # uid存在
    if not uid:
        return func.response_data_xml(request, {'retcode': '10001','reason': u'用户不存在', 'displaynumber': '', 'allowedcalltime': '0'})
    # OTT电话
    if str(calltype)=='1':
        if buss_type==4:
            return func.response_data_xml(request, {'retcode': '0','reason': u'随机聊拨打', 'displaynumber': '', 'allowedcalltime': '-1', 'userData': content.get('userData','') })
        else:
            return func.response_data_xml(request, {'retcode': '0','reason': u'点对点免费拨打', 'displaynumber': '', 'allowedcalltime': '-1', 'userData': content.get('userData','')})
    # 免费电话
    if i_fee==0:
        m_display = buss_type==3 and '17002410853' or ''
        return func.response_data_xml(request, {'retcode': '0','reason': u'0费率免费拨打', 'displaynumber': m_display, 'allowedcalltime': '-1'})
    if number==config.BRAND_SERV_NUMBER[bid]:
        return func.response_data_xml(request, {'retcode': '0','reason': u'客服电话免费拨打', 'displaynumber': '', 'allowedcalltime': '-1'})
    # 账户存在
    try:
        balance = dao.get_balance_obj(bid, uid)
    except:
        logger.error(u"%s-%s not exist in balance table:" % (bid, uid), exc_info=True)
        return func.response_data_xml(request, {'retcode': '10006','reason': u'账户不存在', 'displaynumber': '', 'allowedcalltime': '0'})
    # 账户状态
#    if balance.enable_flag=='0':
#        return func.response_data_xml(request, {'retcode': '10002','reason': u'账户被冻结', 'displaynumber': '', 'allowedcalltime': '0'})
#    
#    if balance.valid_date<=datetime.datetime.now():
#        return func.response_data_xml(request, {'retcode': '10003','reason': u'账户已过期', 'displaynumber': '', 'allowedcalltime': '0'})

    # 账户余额
    balance_value = balance.balance
    if bid in config.GIFT_BALANCE_BRAND:
        # 钱包分离
        if balance.gift_valid_date<=datetime.datetime.now():
            gift_value = 0
        else:
            gift_value = balance.giftbalance
        if balance_value>gift_value:
            cur_money = balance_value + gift_value
        else:
            cur_money = balance_value*2
    else:
        cur_money = balance_value
    # 当前套餐的剩余时长
    cur_long = 0
    if config.TIME_PACKAGE_FLAG:
        if number[:2] in config.NATIONAL_PREFIX or buss_type==3: #国际
            cur_long = 0
        else:
            cur_long = func.get_cur_long_total(bid, uid)/2
    # 总可打时长
    total_long = 0
    # 获取费率
    m_feerate,fee_type = func.get_feerate(bid, uid, number, calltype, userdata)
    ########
    if str(m_feerate)=='0':
        # 零费率情况
        if fee_type=='fn':
            # 亲情号
            fn_val = func.get_fn_val(bid, uid)
            total_long = fn_val>7200 and 7200 or fn_val
        else:
            total_long = 7200
    else:
        total_long = cur_long + (int(cur_money)/int(m_feerate))*60
        logger.info(u'precall_get_result_data [cur_long,cur_money,m_feerate] %s '%str( (cur_long,cur_money,m_feerate) ) )
        total_long = total_long>7200 and 7200 or total_long
        
    if total_long>=60:
        ret_display = func.get_display_number(bid, uid, buss_type, called)
        return func.response_data_xml(request, {'retcode': '0','reason': u'', 'displaynumber': ret_display, 'allowedcalltime': str(total_long)})
    else:
        if fee_type=='fn':
            return func.response_data_xml(request, {'retcode': '10007','reason': u'亲情号拨打时长已用完', 'displaynumber': '', 'allowedcalltime': '0'})
        else:
            return func.response_data_xml(request, {'retcode': '10005','reason': u'余额不足', 'displaynumber': '', 'allowedcalltime': '0'})
        
  
@route('/api/called_notify/',method=["GET","POST"])
@dbop
def called_notify():
    content = func.get_context_data_dict(request)
    async.deal_called_async(content)
    return func.response_data_xml(request, {'retcode': '0','reason': u''})

@route('/version',method=["GET","POST"])
def version():
    start = time.clock()
    res = {
           'result' : 0,
           'reason':u'访问成功',
           'version' : '2.1.0',
           'update_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(__file__))),
           'now' : time.strftime('%Y-%m-%d %H:%M:%S'),
           }
    end =time.clock()
    res["use_time"] = str(end - start)
    return res

