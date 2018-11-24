# -*- coding: utf-8 -*-
import datetime

from models import * 


def get_balance_obj(bid, uid):
    return Balance.get_or_create(brand=bid, uid=uid )

def get_timeacct_now_qs(bid, uid):
    u'''
    获取当前的包时套餐
    '''
    sql = "select * from time_acct where brand_id='%s' and uid=%s and eff_time<=NOW() and exp_time>NOW() order by exp_time"%(bid, uid)
    return Time_Acct.raw(sql)

def get_cur_package(bid, uid):
    qs = get_timeacct_now_qs(bid, uid)
    m_list = [e for e in qs]
    if len(m_list)>0:
        return m_list[0]
    else:
        return None
    
def get_cur_packages(bid, uid):
    qs = get_timeacct_now_qs(bid, uid)
    return qs

def get_fn_feerate(bid):
    u'''
     获取品牌的亲情号费率
    '''
    return T_Fn_Feerate.get( T_Fn_Feerate.brandid==bid )

def check_fn_now(bid, uid):
    u'''
    检查当前是否开通了亲情号服务
    '''
    m_now = datetime.datetime.now()
    return T_Fn_User.select().where( (T_Fn_User.brandid == bid) & (T_Fn_User.uid == uid)  & (T_Fn_User.time <= m_now) & (T_Fn_User.end_time > m_now) ).exists()

def get_fn_number_list(bid, uid):
    u'''
    获取亲情号码
    '''
    qs = T_Fn_Number.select().where( (T_Fn_Number.brandid == bid) & (T_Fn_Number.uid == uid) )
    return [e.number for e in qs]

def get_brand_feerate(bid,number):
    u'''
    根据最长匹配得到费率
    '''
    sql = "select * from tariff where brand_id='%s' and instr('%s',prefix)=1 order by prefix_len desc limit 1"%(bid, number)
    qs = Tariff.raw(sql)
    return [e.unit_fee for e in qs]

def get_call_count_obj(bid, uid):
    return Call_Count.get( (Call_Count.brand==bid) & (Call_Count.uid==uid) )

def incr_call_count(obj):
    obj.callcount = obj.callcount + 1
    obj.save()
    
def add_call_count(bid, uid):
    obj = Call_Count()
    obj.brand = bid
    obj.uid = uid
    obj.ctime = datetime.datetime.now()
    obj.callcount = 1
    obj.calltype = 1
    obj.save()
    
def check_display_now(bid, uid, number, calltype):
    u'''
    检查当前是否开通了来显服务
    '''
    m_now = datetime.datetime.now()
#    # 双11匿名免费电话实现
#    if str(calltype)=='2':
#        if m_now > datetime.datetime(2014,11,11,0,0,0) and m_now < datetime.datetime(2014,11,12,6,0,0):
#            import rpc_call
#            try:
#                ret = rpc_call.get_inviter(uid, number)
#                if ret==False:
#                    return 0
#            except:
#                pass
    return not Servvaliduser.select().where( (Servvaliduser.brand == bid) & (Servvaliduser.uid == uid)  & (Servvaliduser.starttime <= m_now) & (Servvaliduser.endtime > m_now) & (Servvaliduser.status == 2)  ).exists()
    
def have_deal(callid):
    return  Call_Log.select().where( Call_Log.session == callid  ).exists()

def deduct_cur_package(bid, uid, val):
    cur_package = get_cur_package(bid, uid)
    cur_package.month_left_time = cur_package.month_left_time - val
    return cur_package.save()

def deduct_cur_packages(bid, uid, val):
    deduct_val = val
    cur_packages = get_cur_packages(bid, uid)
    for e in cur_packages:
        m_val = e.month_left_time
        if m_val>=deduct_val:
            e.month_left_time = m_val - deduct_val
            e.save()
            break
        else:
            deduct_val = deduct_val - m_val
            e.month_left_time = 0
            e.save()
    return 1

def deduct_balance_val(bid, uid, val, gift_val=0):
    return Balance.update(balance=Balance.balance - val, giftbalance=Balance.giftbalance - gift_val).where( (Balance.brand==bid) & (Balance.uid==uid) ).execute()


def get_call_info_obj(bid, uid):
    return Call_Info.get( (Call_Info.brand==bid) & (Call_Info.uid==uid) )

def update_call_info(bid, uid, call_time, call_long, fee_type):
    try:
        obj = Call_Info.get( (Call_Info.brand==bid) & (Call_Info.uid==uid) )
        if fee_type =='fn':
            if obj.last_call_time.month == datetime.datetime.now().month:
                obj.gift_balance = (obj.gift_balance and obj.gift_balance or 0) + call_long
            else:
                obj.gift_balance = call_long
        obj.last_call_time = call_time
        obj.save()
    except Call_Info.DoesNotExist:
        obj = Call_Info()
        obj.brand = bid
        obj.uid = uid
        obj.ctime = datetime.datetime.now()
        obj.call_success = 'y'
        obj.first_call_time = call_time
        obj.last_call_time = call_time
        if fee_type =='fn':
            obj.gift_balance = call_long
        else:
            obj.gift_balance = 0
        obj.save()
    
def add_call_info(bid, uid):
    pass

def update_call_stat(bid, uid, i_seconds, o_seconds, i_acc_seconds, o_acc_seconds):
    try:
        obj = T_Callstat.get( (Call_Info.brand==bid) & (Call_Info.uid==uid) )
        obj.i_seconds = obj.i_seconds + i_seconds
        obj.o_seconds = obj.o_seconds + o_seconds
        obj.i_acc_seconds = obj.i_acc_seconds + i_acc_seconds
        obj.o_acc_seconds = obj.o_acc_seconds + o_acc_seconds
        obj.save()
    except T_Callstat.DoesNotExist:
        obj = T_Callstat()
        obj.brand = bid
        obj.uid = uid
        obj.i_seconds = i_seconds
        obj.o_seconds = o_seconds
        obj.i_acc_seconds = i_acc_seconds
        obj.o_acc_seconds = o_acc_seconds
        obj.save()
        
def get_new_log():
    new_obj = Call_Log()
    return new_obj

def add_call_log(obj):
    return obj.save()

def get_fn_calltime(bid, uid):
    try:
        obj = Call_Info.get( (Call_Info.brand==bid) & (Call_Info.uid==uid) )
        m_val = obj.gift_balance
        return m_val and m_val or 0
    except Call_Info.DoesNotExist:
        return 0