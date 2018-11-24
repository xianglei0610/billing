# -*- coding: utf-8 -*-

import datetime
import rc4
from XML2Dict import XML2Dict,Dict2XML

import dao
import config
from log_set import logger
import rpc_call

def get_context_data_dict(request):
    if request.method=='POST':
        if request.POST.get('calltype',None):
            return dict(request.POST)
        else:
            xml = XML2Dict()
            data_dict = xml.parse(request.body.read())
        return data_dict["request"]
    else:
        return dict(request.params)
    
def response_data_xml(request,data_dict):
    if request.method=='POST':
        if request.POST.get('calltype',None):
            logger.info(u'response_data %s '%str(data_dict) )
            return data_dict
        else:
            m_data = {'response': data_dict}
            obj = Dict2XML()
            data_xml = obj.parse(m_data)
            logger.info(u'response_data %s '%str(data_xml) )
            return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + data_xml
    else:
        logger.info(u'response_data %s '%str(data_dict) )
        return data_dict

def get_feerate(bid, uid, number, calltype, userdata):
    u'''
    获取费率 calltype  0：直拨，1：免费，2：回拨
    '''
    #透传费率
    if userdata.has_key("data"):
        m_data = userdata["data"]
        if m_data.has_key("fee"):
            #从透传字段中获取费率
            return int(m_data["fee"]),'raw'
        
    #免费电话费率
    if str(calltype)=='1' or number==config.BRAND_SERV_NUMBER[bid]:
        return 0, 'free'
    
    #亲情号费率
    if config.FN_FLAG and rpc_call.check_fn(bid, uid, number):
        return 0, 'fn'
    
    # 固定费率
    if number[:2] in config.NATIONAL_PREFIX: 
        # 国际费率
        feerate_forward = dao.get_brand_feerate(bid, number)[0]
    else:
        # 国内固定费率
        ct = str(calltype)
        brand_feerate = config.BRAND_FEERATE.get(bid, (80000,40000) )
        if ct== '0': #直拨
            feerate_forward = int(brand_feerate[0])
        elif ct== '2': #回拨
            feerate_forward =  int(brand_feerate[1])
        else:
            feerate_forward =  0
    # 回拨B路费率处理
    if str(calltype)=='2':
        feerate_back = config.BRAND_FEERATE.get(bid, (80000,40000) )[1]
        m_feerate = feerate_forward + int(feerate_back)
    else:
        m_feerate = feerate_forward
    return m_feerate, 'common'

def get_display_number(bid, uid, buss_type, called):
    u'''来显号码'''
    display = ''
    if buss_type!=3:
        #非陪聊拨打
        if called[:2] in config.NATIONAL_PREFIX: #国际
            return ''
        display_flag = rpc_call.get_display_status(bid, uid) #来显开关
        if display_flag:
            phone, check = rpc_call.get_phone_from_uid(bid, uid)
            if phone:
                display = phone
#            if not phone or str(check).lower()=='false':
#                #无手机号
#                if str(calltype)=='2':
#                    try:
#                        call_count = dao.get_call_count_obj(bid, uid)
#                        if call_count.callcount> 2:
#                            return func.response_data_xml(request, {'retcode': '10004','reason': u'未绑定手机号超过了拨打次数限制', 'displaynumber': '', 'allowedcalltime': '0'})
#                        dao.incr_call_count(call_count)
#                    except:
#                        dao.add_call_count(bid, uid)
#            else:
#                display = phone
    else:
        #陪聊拨打显示国定的号码
        display = '17002410853'
    return display
        
def get_cur_long(bid, uid):
    u'''
    当前套餐的剩余时长
    '''
    cur_long = 0
    cur_package = dao.get_cur_package(bid, uid)
    if cur_package:
        cur_long = cur_package.month_left_time
    else:
        cur_long = 0
    return cur_long

def get_cur_long_total(bid, uid):
    u'''
    当前套餐的剩余时长
    '''
    cur_long = 0
    cur_packages = dao.get_cur_packages(bid, uid)
    max_expire = datetime.datetime.now()
    if cur_packages:
        for e in cur_packages:
            cur_long += e.month_left_time
            m_exp_time = e.exp_time
            if m_exp_time>max_expire:
                max_expire = m_exp_time
    else:
        cur_long = 0
#    m_diff = max_expire - datetime.datetime.now()
#    diff_total = m_diff.days*24*60*60 + m_diff.seconds
#    if diff_total>0 and cur_long>diff_total:
#        cur_long = diff_total
    return cur_long

def deduct_balance(bid, uid, val):
    if bid in config.GIFT_BALANCE_BRAND:
        m_val = val/2
        balance = dao.get_balance_obj(bid, uid)
        balance_value = balance.balance
        if balance.gift_valid_date<=datetime.datetime.now():
            gift_value = 0
        else:
            gift_value = balance.giftbalance
        if balance_value>gift_value:
            if gift_value>=m_val:
                return dao.deduct_balance_val(bid, uid, m_val, m_val)
            else:
                return dao.deduct_balance_val(bid, uid, val-gift_value, gift_value)
        else:
            return dao.deduct_balance_val(bid, uid, m_val, m_val)
    else:
        return dao.deduct_balance_val(bid, uid, val)
    
def get_fn_val(bid, uid):
    all_val = int(config.FN_LIMIT_CALLTIME)
    fn_calltime = dao.get_fn_calltime(bid, uid)
    logger.info(u'get_fn_calltime%s return %s '%( str( (bid, uid) ),fn_calltime) )
    return all_val - fn_calltime


def parse_data(content):
    u'''解析userData透传内容'''
    res = {}
    m_list = content.split('|')
    for e in m_list:
        m_item = e.split('@')
        res[m_item[0]] = m_item[1]
    return {'data':res}

def uncode_pwd(rc4_password,stype=False):
    '''将rc4加密后的密码，解密出来
    '''
    if stype:
        res = {}
        m_list = rc4_password.split('|')
        for e in m_list:
            m_item = e.split('@')
            res[m_item[0]] = m_item[1]
        return {'data':res}
    else:
        key = config.AMS_CONFIG["AMS_KEY"]
        real_password = rc4.decode(rc4_password, key)
        return real_password