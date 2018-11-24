# -*- coding: utf-8 -*-
import functools
import copy
import datetime

from peewee import *
from pool import PooledMySQLDatabase

import config

m_config = copy.deepcopy(config.DB_CONF)
m_config.pop("db", None)
m_config["port"] = int(m_config["port"])
database = PooledMySQLDatabase(config.DB_CONF["db"], threadlocals=True ,max_connections=50, stale_timeout=600, **m_config)

#database = PooledMySQLDatabase(config.DB_NAME, threadlocals=True ,max_connections=50, stale_timeout=600, **{'host': config.DB_HOST, 'port':config.DB_PORT, 'user': config.DB_USER, 'passwd': config.DB_PWD})

def dbop(func, *args, **kwargs):
    '''限制IP'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with database:
            return func(*args, **kwargs)
    return wrapper

class UnknownFieldType(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

def get_default_validdate():
    return datetime.datetime.now()+datetime.timedelta(days=30)

class Balance(BaseModel):
    u'''账户余额表'''
    
    uid = BigIntegerField(verbose_name=u'用户uid')
    brand = CharField(verbose_name=u'商户id', db_column='brand_id')
    acct = PrimaryKeyField(verbose_name=u'自动增长', db_column='acct_id')
    balance = BigIntegerField(null=True, verbose_name=u'账户余额', default=0)
    valid_date = DateTimeField(verbose_name=u'余额有效期', default=get_default_validdate)
    create_time = DateTimeField(verbose_name=u'账户创建日期', default=datetime.datetime.now)
    enable_flag = CharField(null=True, verbose_name=u'冻结状态标志', default=1)
    giftbalance = BigIntegerField(null=True, verbose_name=u'赠送账户余额', default=0)
    gift_valid_date = DateTimeField(null=True, verbose_name=u'赠送余额有效期')
    reserve1 = BigIntegerField(null=True, verbose_name=u'保留字段1', db_column='Reserve1')
    reserve2 = CharField(null=True, verbose_name=u'保留字段2', db_column='Reserve2')


    class Meta:
        db_table = 'balance'

class Call_Info(BaseModel):
    u'''用户统计表'''
    
    uid = BigIntegerField(verbose_name=u'用户uid')
    brand = CharField(verbose_name=u'品牌', db_column='brand_id')
    balance = BigIntegerField(null=True, verbose_name=u'费用')
    gift_balance = BigIntegerField(null=True, verbose_name=u'赠送费用')
    call_success = CharField(null=True, verbose_name=u'是否呼叫成功:y/n')
    call_type = CharField(verbose_name=u'呼叫类型 callback回拨; direct直拨')
    first_call_time = DateTimeField(null=True, verbose_name=u'首次呼叫时间')
    last_call_time = DateTimeField(verbose_name=u'最后呼叫时间')
    phone_number = CharField(verbose_name=u'手机号码')

    class Meta:
        db_table = 'call_info'

class Call_Log(BaseModel):
    u'''话单(计费记录)'''
    
    call = PrimaryKeyField(verbose_name=u'话单id', db_column='call_id')
    session = CharField(verbose_name=u'计费系统计费ID', db_column='session_id')
    brand = CharField(verbose_name=u'商户', db_column='brand_id')
    
    from_number = CharField(verbose_name=u'Sip协议主叫号码')
    to_number = CharField(verbose_name=u'Sip协议被叫号码')
    
    from_ip = CharField(null=True, verbose_name=u'软交换呼叫来源IP')
    to_ip = CharField(null=True, verbose_name=u'送出的IP')
    
    start_time = DateTimeField(verbose_name=u'计费开始时间')
    end_time = DateTimeField(null=True, verbose_name=u'计费结束时间')
    
    call_time = IntegerField(verbose_name=u'计费时长')
    pkg_call_time = IntegerField(verbose_name=u'包月套餐时间')
    billing_time = IntegerField(verbose_name=u'费时长计')
    
    field_rate = CharField(verbose_name=u'账户计费费率')
    field_units = IntegerField(verbose_name=u'账户计费单元')
    field_fee = BigIntegerField(verbose_name=u'账户计费费用')
    
    call_year = IntegerField(verbose_name=u'呼叫年份', default=0)
    call_month = IntegerField(verbose_name=u'呼叫月份', default=0)
    #############################################
    
    call_hour = IntegerField(verbose_name=u'呼叫小时')
    call_week = IntegerField(verbose_name=u'呼叫的星期')

    gate_discount = IntegerField(verbose_name=u'落地网关折扣')
    gate_fee = BigIntegerField(verbose_name=u'落地网关计费费用')
    gate = IntegerField(verbose_name=u'落地网关ID', db_column='gate_id')
    gate_name = CharField(verbose_name=u'落地网关名称')
    gate_rate = CharField(verbose_name=u'落地网关计费费率')
    gate_units = IntegerField(verbose_name=u'落地网关计费单元')

    agent_discount = IntegerField(verbose_name=u'代理商折扣')
    agent_fee = BigIntegerField(verbose_name=u'代理商计费费用')
    agent = IntegerField(verbose_name=u'代理商ID', db_column='agent_id')
    agent_name = CharField(verbose_name=u'代理商名称')
    agent_rate = CharField(verbose_name=u'代理商计费费率')
    agent_units = IntegerField(verbose_name=u'代理商计费单元')

    call_date = DateField(verbose_name=u'呼叫日期')
    call_day = IntegerField(verbose_name=u'呼叫的天数')
    call_type = CharField(verbose_name=u'呼叫类型')
    e_bye = CharField(null=True)
    e_ok = CharField(null=True)
    field_discount = IntegerField(verbose_name=u'账户折扣')
    field = IntegerField(verbose_name=u'账户Field_id', db_column='field_id')
    field_name = CharField(verbose_name=u'账户姓名')

    long_name = CharField(verbose_name=u'用户姓名')
    raw_from_number = CharField(null=True, verbose_name=u'号码替换后的主叫号码')
    raw_to_number = CharField(null=True, verbose_name=u'号码替换后的被叫号码')
    time_type = CharField(verbose_name=u'时间类型')
    user = IntegerField(verbose_name=u'用户user_id', db_column='user_id')

    class Meta:
        db_table = 'call_log'
        table_split = 'day'
        
class Call_Log_Next(Call_Log):
    class Meta:
        db_table = 'call_log'
        table_split = 'day'
        table_next = True

class Charge_Log(BaseModel):
    u'''充值日志记录表'''
    
    balance = BigIntegerField(null=True)
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    charger = IntegerField(verbose_name=u' 充值者ID', db_column='charger_id')
    charger_level = IntegerField(verbose_name=u' 充值者级别')
    charger_name = CharField(null=True, verbose_name=u'支付者姓名')
    fee_type = CharField(null=True, verbose_name=u'扣费类型')
    giftbalance = BigIntegerField(null=True)
    log = BigIntegerField(verbose_name=u'支付日志ID', db_column='log_id')
    money = BigIntegerField(verbose_name=u' 支付金额')
    order = CharField(null=True, verbose_name=u'订单号', db_column='order_id')
    remark = CharField(null=True, verbose_name=u' 备注')
    time = DateTimeField(null=True, verbose_name=u'支付时间')
    uid = BigIntegerField(verbose_name=u'用户UID')
    way = IntegerField(verbose_name=u'充值方式')

    class Meta:
        db_table = 'charge_log'


class Kc_Fee(BaseModel):
    u'''费率表'''
    
    feeid = BigIntegerField(verbose_name=u'短信扣费ID', db_column='fee_id')
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    uid = BigIntegerField(verbose_name=u'用户UID')
    fee = BigIntegerField(verbose_name=u' 短信扣费费用')
    fee_type = IntegerField(verbose_name=u'扣费类型')
    remark = CharField(null=True, verbose_name=u'备注')
    time = DateTimeField(null=True, verbose_name=u' 短信扣费时间')

    class Meta:
        db_table = 'kc_fee'

class Package(BaseModel):
    u'''套餐表'''
    package = IntegerField(verbose_name=u'包月套餐ID', db_column='package_id')
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    package_name = CharField(null=True, verbose_name=u'套餐名称')
    package_describe = CharField(null=True, verbose_name=u'套餐描述')
    day_total_time = IntegerField(verbose_name=u'日限制')
    effect_time = IntegerField(verbose_name=u'有效期')
    prefix = CharField(null=True, verbose_name=u'限制区域')
    level = IntegerField(verbose_name=u'套餐等级')
    money = IntegerField(verbose_name=u'支付币种', db_column='money_id')
    money_number = IntegerField(verbose_name=u'支付数量')
    call_time = IntegerField(verbose_name=u'可打时间')
    grant_time = IntegerField(verbose_name=u'额外赠送')
    package_type = IntegerField(verbose_name=u'套餐类型')


    class Meta:
        db_table = 'package'

class Package_Used_Record(BaseModel):
    brand = CharField(verbose_name=u'品牌id', db_column='brand_id')
    buy_time = DateTimeField(null=True, verbose_name=u'购买时间')
    clear_time = DateTimeField(verbose_name=u'清理时间')
    id = BigIntegerField(verbose_name=u'记录ID')
    left_time = BigIntegerField(null=True, verbose_name=u'剩余时间')
    package = IntegerField(verbose_name=u'套餐编号', db_column='package_id')
    uid = BigIntegerField(verbose_name=u'UID')

    class Meta:
        db_table = 'package_used_record'

class Recharge_Info(BaseModel):
    brand = CharField(verbose_name=u'商户', db_column='brand_id')
    order = CharField(null=True, verbose_name=u'订单号', db_column='order_id')
    recharge_amount = IntegerField(verbose_name=u'最后充值金额')
    recharge_count = IntegerField(verbose_name=u'累计充值次数')
    recharge_sum = BigIntegerField(verbose_name=u'累计充值金额')
    recharge_time = DateTimeField(verbose_name=u'最后充值时间')
    uid = BigIntegerField(verbose_name=u'uid')

    class Meta:
        db_table = 'recharge_info'

class Servusedlog(BaseModel):
    brand = CharField(db_column='brand_id')
    createdate = DateTimeField(verbose_name=u'扣费日期', db_column='createDate')
    endtime = DateTimeField(verbose_name=u'结束时间', db_column='endTime')
    fee = DecimalField(verbose_name=u'费用')
    open_way = CharField(null=True, verbose_name=u'开通方式(购买=buy,赠送=gift)')
    order = CharField(verbose_name=u'订单编号', db_column='order_id')
    starttime = DateTimeField(verbose_name=u'开始时间', db_column='startTime')
    stoptime = DateTimeField(null=True)
    uid = BigIntegerField(verbose_name=u'用户id')

    class Meta:
        db_table = 'servusedlog'

class Servvaliduser(BaseModel):
    u'''来显表'''
    brand = CharField(db_column='brand_id')
    uid = BigIntegerField(verbose_name=u'用户id')
    endtime = DateTimeField(verbose_name=u'结束时间', db_column='endTime')
    starttime = DateTimeField(verbose_name=u'开始时间', db_column='startTime')
    flag = IntegerField(verbose_name=u'0为未开启,1为有服务没定制, 2为有服务有定制 (2自动续费,1到期自动停止) ')
    open_way = CharField(null=True, verbose_name=u'开通方式(购买=buy,赠送=gift)')
    phonenumber = CharField(null=True, verbose_name=u'绑定手机号', db_column='phoneNumber')
    status = IntegerField(null=True, verbose_name=u'来显状态 1 开通 2 关闭')
    stoptime = DateTimeField(null=True)
    tips = IntegerField(null=True, verbose_name=u'是否到期前提醒')

    class Meta:
        db_table = 'servvaliduser'

class T_Call_Collect(BaseModel):
    u'''用户呼叫汇总'''

    brand = CharField(db_column='brand_id')
    call_count = BigIntegerField(null=True, verbose_name=u'累计呼叫次数')
    first_call_time = DateTimeField(null=True, verbose_name=u'首次体验时间')
    i_acc_seconds = IntegerField(verbose_name=u'拨打国内的计费时长累加')
    i_seconds = IntegerField(verbose_name=u'拨打国内时长累加')
    id = BigIntegerField()
    last_call_time = DateTimeField(null=True, verbose_name=u'最后体验时间')
    o_acc_seconds = IntegerField(verbose_name=u'拨打国际的计费时长累加')
    o_seconds = IntegerField(verbose_name=u'拨打国际时长累加')
    uid = BigIntegerField()

    class Meta:
        db_table = 't_call_collect'

class T_Caller(BaseModel):
    number = CharField()
    time = DateTimeField()
    uid = IntegerField()

    class Meta:
        db_table = 't_caller'

class T_Callstat_201412(BaseModel):
    brand = CharField(db_column='brand_id')
    seconds = IntegerField()
    uid = BigIntegerField()

    class Meta:
        db_table = 't_callstat_201412'

class T_Fn_Feerate(BaseModel):
    brandid = CharField()
    callback = IntegerField()
    directcall = IntegerField()
    remark = CharField()

    class Meta:
        db_table = 't_fn_feerate'

class T_Fn_Modify_Log(BaseModel):
    brandid = CharField()
    id = BigIntegerField()
    new_number = CharField(null=True)
    old_number = CharField(null=True)
    time = DateTimeField(null=True)
    uid = BigIntegerField()

    class Meta:
        db_table = 't_fn_modify_log'

class T_Fn_Number(BaseModel):
    brandid = CharField()
    id = BigIntegerField()
    number = CharField(null=True)
    time = DateTimeField(null=True)
    uid = BigIntegerField()

    class Meta:
        db_table = 't_fn_number'

class T_Fn_Open_Log(BaseModel):
    brandid = CharField()
    day = IntegerField(null=True)
    id = BigIntegerField()
    month = IntegerField(null=True)
    orderid = CharField()
    time = DateTimeField(null=True)
    uid = IntegerField()
    year = IntegerField(null=True)

    class Meta:
        db_table = 't_fn_open_log'

class T_Fn_User(BaseModel):
    brandid = CharField()
    uid = BigIntegerField()
    max_num = IntegerField()
    time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)


    class Meta:
        db_table = 't_fn_user'

class T_Safety(BaseModel):
    u'''防重复'''

    brand = CharField(db_column='brand_id')
    business = CharField(verbose_name=u'业务码')
    order = CharField(db_column='order_id')
    order_time = DateTimeField(verbose_name=u'订单时间')

    class Meta:
        db_table = 't_safety'

class Tariff(BaseModel):
    area_name = CharField(verbose_name=u' 计费国家名称')
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    call_type = CharField(verbose_name=u'费率计费类型')
    caller_prefix = CharField(verbose_name=u' 计费主叫号码前缀')
    caller_prefix_len = IntegerField(verbose_name=u'计费主叫号码前缀长度')
    discount_flag = CharField(verbose_name=u' 折扣是否允许')
    enable_flag = CharField(null=True, verbose_name=u'激活标志')
    first_fee = IntegerField(verbose_name=u'第一时段计费费率')
    first_time = IntegerField(verbose_name=u'第一时段计费计费时间')
    min_money = IntegerField(verbose_name=u'最小通话金额')
    prefix = CharField(verbose_name=u'计费前缀')
    prefix_len = IntegerField(verbose_name=u'计费前缀长度')
    tariff = IntegerField(verbose_name=u'auto_increment', db_column='tariff_id')
    unit_fee = IntegerField(verbose_name=u'计费单位费率')
    unit_time = IntegerField(verbose_name=u' 计费单位时间')

    class Meta:
        db_table = 'tariff'

class Time_Acct(BaseModel):
    u'''用户套餐表'''
    acct = PrimaryKeyField(verbose_name=u'账号ID', db_column='acct_id')
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    uid = BigIntegerField(verbose_name=u'用户UID')
    month_left_time = IntegerField(verbose_name=u'包月月剩余时间')
    day_left_time = IntegerField(verbose_name=u'包月每天剩余通话时长')
    day_total_time = IntegerField(verbose_name=u'包月每天限制通话时长')
    eff_time = DateTimeField(verbose_name=u'生效时间')
    exp_time = DateTimeField(verbose_name=u'失效时间')
    last_call_time = DateTimeField(verbose_name=u'最后一次通话时间')

    package = BigIntegerField(verbose_name=u'套餐id', db_column='package_id')
    package_name = CharField(null=True, verbose_name=u'套餐名称')
    package_type = IntegerField(verbose_name=u'套餐类型')
    prefix = CharField(verbose_name=u'被叫前缀')

    class Meta:
        db_table = 'time_acct'

class User(BaseModel):
    ctime = DateTimeField(null=True)
    name = CharField()
    number = CharField(null=True)
    prefix = CharField(null=True)
    pwd = CharField()
    state = CharField(null=True)

    class Meta:
        db_table = 'user'

class User_Package(BaseModel):
    id = BigIntegerField()
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    uid = BigIntegerField(verbose_name=u'用户UID')
    buy_time = DateTimeField(verbose_name=u'默认启用时间')
    use_type = IntegerField(verbose_name=u'使用类型,1未启用状态')
    package = IntegerField(verbose_name=u'包月套餐号', db_column='package_id')
    number = IntegerField(verbose_name=u'包月数')
    prefix = CharField(verbose_name=u'限制区域号')


    class Meta:
        db_table = 'user_package'

class Vipopenlog(BaseModel):
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    orderid = CharField(verbose_name=u'订单号')
    type = IntegerField(verbose_name=u'vip类型')
    uid = BigIntegerField(verbose_name=u'用户UID')

    class Meta:
        db_table = 'vipopenlog'

class Viprebundlog(BaseModel):
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    date = DateTimeField(verbose_name=u'返还时间')
    fee = CharField(verbose_name=u'返还费用')
    rebundtime = IntegerField(verbose_name=u'返还分钟', db_column='rebundTime')
    timetype = CharField(verbose_name=u'返还时段', db_column='timeType')
    uid = BigIntegerField(verbose_name=u'用户UID')

    class Meta:
        db_table = 'viprebundlog'

class Viptemp(BaseModel):
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    free_day = DateField(verbose_name=u'享受狂欢特权日期')
    uid = BigIntegerField(verbose_name=u'用户UID')

    class Meta:
        db_table = 'viptemp'

class Vipuser(BaseModel):
    brand = CharField(verbose_name=u'品牌ID', db_column='brand_id')
    uid = BigIntegerField(verbose_name=u'用户UID')
    valid_time = DateTimeField(verbose_name=u'到期时间')

    class Meta:
        db_table = 'vipuser'

class White_List(BaseModel):
    brand = CharField(null=True, db_column='brand_id')
    number = CharField()
    type = CharField()

    class Meta:
        db_table = 'white_list'

class Call_Count(BaseModel):
    brand = CharField(null=True, db_column='brand_id')
    callcount = IntegerField(null=True)
    calltype = IntegerField(null=True)
    ctime = DateTimeField(null=True)
    uid = BigIntegerField(null=True)

    class Meta:
        db_table = 'call_count'
        
class T_Callstat(BaseModel):
    brand = CharField(db_column='brand_id')
    i_acc_seconds = IntegerField()
    i_seconds = IntegerField()
    o_acc_seconds = IntegerField()
    o_seconds = IntegerField()
    seconds = IntegerField()
    uid = BigIntegerField()

    class Meta:
        db_table = 't_callstat'
        table_split = 'month'
        #primary_key = CompositeKey('brand', 'uid')
        
class T_Callstat_Next(T_Callstat):
    class Meta:
        db_table = 't_callstat'
        table_split = 'month'
        table_next = True