# -*- coding: utf-8 -*-

#数据库连接
DB_CONF = {
            'host':'172.16.12.76', # 数据库地址
            'port':3306,
            'user':'root', # 数据库 登录账号
            'passwd':'keepc@2014', # 数据库 登录密码
            'db':'bc', # 数据库 库名
            'charset':'utf8'
           }

# Redis连接配置
USER_REDIS_CONF = {
              'HOST' : '117.121.21.90',
              'PORT' : 6301,
              'PASSWORD' : ''
              }


# 是否开启亲情号功能
FN_FLAG = False

# 含赠送账户的品牌
GIFT_BALANCE_BRAND = ( 'uu', '4g', 'ly' )

# 直拨/回拨费率配置
BRAND_FEERATE = {
                    'vs': (100000,75000)
                 }

# 客服号码配置(打客服电话免费)
BRAND_SERV_NUMBER = {
                    'vs': '075561363066'
                 }

# appid和品牌映射关系
APPID_TO_BID = {
                '4a80d707ba4044d38e6a2532c5b37a52': 'vs',   # 线上
                '8ff9da33f46b44919c2232228f0891ce': 'vs', # 测试
                }

NATIONAL_PREFIX = ('00',)#('0086', '0083', '0087')

# AMS接口参数配置
#AMS_CONFIG= { 
#         "AMS_URL":"http://202.105.136.109:8180/ams/", # AMS 的访问地址
#         "AMS_KEY":"1bb762f7ce24ceee",  # AMS 对密码 rc4 加密时用
#         "key":"keepc_mobilephone!@#456", # 客户端对密码 rc4 加密时用(注意跟 AMS 的加密值不同)
#         "MAC_KEY":"0859db5b7b8ae8fe4b0d344af4d11199", # AMS 对应的 mac_key
#         "MAC_IP" : "127.0.0.1", # ams 对应的 macip
#        }

#def make_config(globals_var):
#    import os
#    import json
#    import urllib
#    
#    from oe import vars
#    if os.path.exists('./config.json'):
#        jsonobject = json.load(file('./config.json'))
#    else:
#        f=urllib.urlopen(vars.CONFIG_GET_URL+"?app_key=billing")
#        json_str=f.read()
#        jsonobject = json.loads(json_str)
#    for key,val in jsonobject.iteritems():
#        globals_var[key] = val
from oe import vars  
vars.make_config( globals(), "billing")

TIME_PACKAGE_FLAG = False
