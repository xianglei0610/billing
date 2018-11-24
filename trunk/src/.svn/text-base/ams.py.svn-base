#!/usr/local/bin/python
#coding=utf-8
'''
AMS帐号管理系统API接口
@author: yaoshiyan
'''
import urllib2
import urllib
from hashlib import md5
import datetime
import random
import logging
import time

#import httplib2

import config #from main import config

#http = httplib2.Http()

_UTF8_TYPES = (bytes, type(None))

def get_config(bid,key):
    return config.AMS_CONFIG.get(key)

def utf8(value):
    if isinstance(value, _UTF8_TYPES):
        return value
    assert isinstance(value, unicode)
    return value.encode("utf-8")

def rc4(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    return ''.join(out)

def hex2str(s):
    '''16进制转字符串'''
    if s[:2] == '0x' or s[:2] == '0X':
        s = s[2:]
    res = ""
    for i in range(0, len(s), 2):
        hex_dig = s[i:i + 2]
        res += (chr(int(hex_dig, base=16)))
    return res


def str2hex(string):
    '''字符串转16进制'''
    res = ""
    for s in string:
        hex_dig = hex(ord(s))[2:]
        if len(hex_dig) == 1:
            hex_dig = "0" + hex_dig
        res += hex_dig
    return res

def uncode_pwd(brandid, rc4_password, key_type='ams'):
    '''将rc4加密后的密码，解密出来
    @param {String} brandid 品牌
    @param {String} rc4_password RC4加密后的密码
    @param {String} key_type 加密类型，可选值为：ams(默认值), client
    '''
    key = ''
    if key_type == 'ams':
        key = get_config(brandid, 'AMS_KEY')#config.SETTINGS.get(brandid, {}).get('AMS_KEY') or config.SETTINGS['all']['AMS_KEY']
    elif key_type == 'client':
        key = get_config(brandid, 'key')#config.SETTINGS.get(brandid, {}).get('key') or config.SETTINGS['all']['key']
    real_password = rc4(hex2str(rc4_password), key)
    return real_password

def encode_pwd(brandid, real_password, key_type='ams'):
    '''将明文密码，用rc4加密
    @param {String} brandid 品牌
    @param {String} real_password 明文的密码
    @param {String} type 加密类型，可选值为：ams(默认值), client
    '''
    key = ''
    if key_type == 'ams':
        key = get_config(brandid, 'AMS_KEY')#config.SETTINGS.get(brandid, {}).get('AMS_KEY') or config.SETTINGS['all']['AMS_KEY']
    elif key_type == 'client':
        key = get_config(brandid, 'key')#config.SETTINGS.get(brandid, {}).get('key') or config.SETTINGS['all']['key']
    rc4_password = str2hex(rc4(real_password, key))
    return rc4_password

def getAmsResp(brandid, amsFunc, params):
    start_time = long(time.time() * 1000)
    AMS_URL = config.AMS_URL#config.SETTINGS.get(brandid, {}).get('AMS_URL') or config.SETTINGS['all']['AMS_URL']
    url = AMS_URL + '/ams/' + amsFunc + "?" + params + "&" + getAmsSign(brandid)
    try:
        f = urllib2.urlopen(url)
        res = f.read()
        f.close()
        #response, res = http.request(url)
        finish_time = long(time.time() * 1000)
        logging.info(u"AMS:%s;结果:%s;时间:%s ms" % (url, res, str(finish_time - start_time)))
        return urlCode2Dict(res)
    except:
        logging.error(u"AMS ERROR: Time out: %s" % url, exc_info=True)
        return {"code": 911}

def urlCode2Dict(result):
    '''ams返回url串转换成dict'''
    return dict(x.split('=') for x in result.split('&'))

def getRand():
    n = datetime.datetime.now().strftime("%H%M%S")
    m = str(random.randint(1000, 9999))
    return n + m

def getAmsSign(brandid):
    macdate = datetime.datetime.now().strftime("%Y%m%d")
    macrand = getRand()
    macip = get_config(brandid, 'MAC_IP')#config.SETTINGS.get(brandid, {}).get('MAC_IP') or config.SETTINGS.get('all', {}).get('MAC_IP', '127.0.0.1')
    MAC_KEY = get_config(brandid, 'MAC_KEY')#config.SETTINGS.get(brandid, {}).get('MAC_KEY') or config.SETTINGS.get('all', {}).get('MAC_KEY', '')
    mac = md5(macip + macdate + macrand + MAC_KEY).hexdigest()
    mac_dict = {"macip":macip,
               "macdate":macdate,
               "macrand":macrand,
               "mac":mac}
    return urllib.urlencode(mac_dict)

def info(brandid, accounttype, account):
    '''查询kc/手机/密码
      建议缓存此结果，同时提供清除缓存的调用方式(以便修改密码后立即生效)
    '''
    param = urllib.urlencode({"brandid": brandid,
                              "accounttype": accounttype,
                              "account": account})
    return getAmsResp(brandid, "info.act", param)

def detail_info(brandid, accounttype, account):
    '''查询用户详细信息'''
    param = urllib.urlencode({"brandid": brandid,
                              "accounttype": accounttype,
                              "account": account})
    return getAmsResp(brandid, "detailinfo.act", param)

def login(brandid, loginType, account, password, loginfrom, ip, platform, pv, v, ptype='', netmode='', buss=''):
    '''登录认证'''
    param = urllib.urlencode({"brandid": brandid,
                              "loginType": loginType,
                              "account": account,
                              "password": password, #md5加密后的密码
                              "from": loginfrom,
                              "ip": ip,
                              "pform":platform,
                              "psystem":pv,
                              "cversion":v,
                              "ptype":utf8(ptype),
                              "netmode":netmode,
                              "buss" : buss, # buss=1 区别为 伪绑定 手机号的
                              })
    return getAmsResp(brandid, "login.act", param)

def choose(brandid, ip):
    '''选号'''
    return getAmsResp(brandid, "choose.act", "ip=%s&brandid=%s" % (ip, brandid))

def kcreg(brandid, uid, password, random, invitedby, invitedflag, regfrom, platform, pv, v, phone_model):
    '''注册'''
    param = urllib.urlencode({"brandid": brandid,
                              "uid": uid,
                              "password": password,
                              "random": random,
                              "invitedby": invitedby,
                              "invitedflag": invitedflag,
                              "regfrom": regfrom,
                              "pform":platform,
                              "psystem":pv,
                              "cversion":v,
                              "ptype":utf8(phone_model),
                              })
    return getAmsResp(brandid, "kcreg.act", param)

def automobilereg(brandid, number, invitedby, invitedflag, regfrom, ip, platform, pv, v, phone_model, ext=''):
    '''自动注册'''
    param = urllib.urlencode({"brandid": brandid,
                              "number": number,
                              "invitedby": invitedby,
                              "invitedflag": invitedflag,
                              "from": regfrom,
                              "ip": ip,
                              "pform":platform,
                              "psystem":pv,
                              "cversion":v,
                              "ptype":utf8(phone_model),
                              "ext": ext})
    return getAmsResp(brandid, "automobilereg.act", param)

def thirdreg(brandid, openid, opentype, invitedby, invitedflag,
             regfrom, ip, platform, pv, v, ptype, ext=''):
    '''第三方帐号自动注册'''
    param = urllib.urlencode({"brandid": brandid,
                              "openid": openid,
                              "opentype": opentype,
                              "invitedby": invitedby,
                              "invitedflag": invitedflag,
                              "from": regfrom,
                              "ip": ip,
                              "pform":platform,
                              "psystem":pv,
                              "cversion":v,
                              "ptype":utf8(ptype),
                              "ext": ext})
    return getAmsResp(brandid, "thirdreg.act", param)

def thirdregnocheck(brandid, device_id, openid, opentype, invitedby, invitedflag, regfrom, ip, platform, pv, v, ptype, ext=''):
    '''第三方帐号自动注册'''
    param = urllib.urlencode({"brandid": brandid,
                              "deviceid" : device_id, # 设备号（手机终端必填）
                              "openid": openid, # 第三方账号(根据access_token从oauthserver获取)
                              "opentype": opentype,
                              "invitedby": invitedby,
                              "invitedflag": invitedflag,
                              "from": regfrom, # 来源：web/mini/mobile
                              "ip": ip,
                              "pform":platform, # mobile/pc
                              "psystem":pv, # 平台：web/mini/android/..
                              "cversion":v,
                              "ptype":utf8(ptype),
                              "ext": ext})
    return getAmsResp(brandid, "thirdregnocheck.act", param)

def thirdbind(brandid, openid, opentype, regfrom, ip,
              platform, uid, pv, v, ptype, ext=''):
    '''第三方帐号绑定'''
    param = urllib.urlencode({"brandid": brandid,
                              "openid": openid,
                              "opentype": opentype,
                              "from": regfrom,
                              "ip": ip,
                              "pform":platform,
                              "uid":uid,
                              "psystem":pv,
                              "cversion":v,
                              "ptype":utf8(ptype),
                              "ext": ext})
    return getAmsResp(brandid, "thirdbind.act", param)

def emailbind(brandid, uid, email, pv):
    """邮箱绑定"""
    param = urllib.urlencode({"brandid":brandid,
                             "account":uid,
                             "accounttype":"kc",
                             "email":email,
                             "from":pv}
                             )
    return getAmsResp(brandid, "sendbindmail.act", param)

def mobilereg(brandid, number, invitedby, invitedflag, regfrom, ip, platform, pv, v, phone_model, ext=''):
    '''短信注册'''
    param = urllib.urlencode({"brandid": brandid,
                              "number": number, # 手机号
                              "invitedby": invitedby, #邀请人UID
                              "invitedflag": invitedflag, #区分推荐人是联盟还是普通UID:kc/1(联盟)/2(新联盟)
                              "from": regfrom,#来源：web/mini/mobile
                              "ip": ip,#客户端ip（web端必填）
                              "pform":platform, #mobile/pc
                              "psystem":pv,#平台：web/mini/android/..
                              "cversion":v,#版本
                              "ptype":utf8(phone_model), # 手机型号
                              "ext": ext,
                              })
    return getAmsResp(brandid, "mobilereg.act", param)

def nobind_phone_reg(brandid, phone, invitedby, invitedflag, regfrom, ip, platform, pv, v, phone_model, partner, type, device_id, sm, code, ext=''):
    '''伪绑定手机的注册'''
    param = {"brandid": brandid,
                              "number": phone, # 手机号码
                              "deviceid" : device_id, # 设备号（手机终端必填）
                              "invitedby": invitedby, #邀请人UID
                              "invitedflag": invitedflag, #区分推荐人是联盟还是普通UID:kc/1(联盟)/2(新联盟)
                              "from": regfrom,#来源：web/mini/mobile
                              "ip": ip,#客户端ip（web端必填）
                              "pform":platform, #mobile/pc
                              "psystem":pv,#平台：web/mini/android/..
                              "ptype":utf8(phone_model), # 手机型号
                              "cversion":v,#版本
                              "partner" : partner, # 个性化的短信模板标识：如拉新，可以传lx,系统在后台配置关于拉新的短信模板即可
                              "sm" : sm, # 自定义的短信模板（不建议用）
                              "type" : type, # 通知类型：  1：语音下发验证码，0或者空：短信
                              "ext": ext,
                              }
    url = 'mobileregnocheck.act'
    # 有验证码的,会直接绑定手机号
    if code:
        url = "mobileregsubmitnopwd.act"
        param['verifyCode'] = code
    param = urllib.urlencode(param)
    return getAmsResp(brandid, url, param)

def reg_validate(brandid, account, ip, type):
    """获取验证码(伪绑定注册,注册超次数时用)"""
    param = urllib.urlencode({"brandid": brandid,
                              "number": account, # 手机号码  1开头的11位数字（国内手机号）；00开头的数字（带国际区号的手机号）
                              "ip": ip, # 客户端IP
                              "type": type, # 1：语音下发验证码，0或者空：短信
                              })
    return getAmsResp(brandid, "mobileregvalidate.act", param)

def emailreg(brandid, email, password, invitedby, invitedflag, regfrom, ip, platform, pv, v, phone_model, ext=''):
    '''短信注册'''
    param = urllib.urlencode({"brandid": brandid,
                              "email": email,
                              "password": password,
                              "invitedby": invitedby,
                              "invitedflag": invitedflag,
                              "from": regfrom,
                              "ip": ip,
                              "pform":platform,
                              "psystem":pv,
                              "cversion":v,
                              "ptype":utf8(phone_model),
                              "ext": ext})
    return getAmsResp(brandid, "emailreg.act", param)

def bindapply(brandid, number, uid, password, type='0'):
    '''绑定请求'''
    param = urllib.urlencode({"brandid": brandid,
                              "number": number,
                              "uid": uid,
                              "password": password,
                              "type": type,
                              })
    return getAmsResp(brandid, "bindapply.act", param)

def bindsubmit(brandid, uid, number, verifyCode):
    '''提交绑定'''
    param = urllib.urlencode({"brandid": brandid,
                              "number": number,
                              "uid": uid,
                              "verifyCode": verifyCode})
    return getAmsResp(brandid, "bindsubmit.act", param)

def bind_phone(brandid, uid, phone, code, shownum):
    '''绑定手机(伪绑定的用)'''
    param = urllib.urlencode({"brandid": brandid,
                              "uid": uid,
                              "number": phone,
                              "verifyCode": code, # 验证码，30分钟内有效
                              "buss": '1', # 标识新注册流程的绑定,原来的注册接口不变
                              #"ext": ext,
                              "xhflag" : shownum,
                              })
    return getAmsResp(brandid, "bindsubmit.act", param)

def reset_pwd_apply(brandid, account):
    '''获取验证码(重置密码用)'''
    param = urllib.urlencode({"brandid": brandid,
                              "number": account, # 手机号码
                              })
    return getAmsResp(brandid, "resetpwdapply.act", param)

def reset_passwd(brandid, account, code,  passwd):
    '''重置密码'''
    param = urllib.urlencode({"brandid": brandid,
                              "number": account, # 手机号码
                              "verifyCode" : code, # 验证码，30分钟内有效
                              "pwd" : passwd, # Rc4加密的密码
                              })
    return getAmsResp(brandid, "resetpwdsubmit.act", param)

def changepwd(brandid, uid, oldpwd, newpwd):
    '''修改密码'''
    param = urllib.urlencode({"brandid": brandid,
                              "uid": uid,
                              "oldpassword": oldpwd,
                              "newpassword": newpwd})
    return getAmsResp(brandid, "changepassword.act", param)

def email_find_pwd(brandid, email):
    '''使用email地址，找回密码'''
    param = urllib.urlencode({"brandid":brandid, "email": email})
    return getAmsResp(brandid, "emailpwd.act", param)

def check_pwd(brandid, type, account, md5pwd):
    if not account or account == 'null' or not account.isdigit():
        return {"result": 1}
    if len(str(account)) == 11 and str(account)[0] == '1':
        type = 'mobile'
    res = info(brandid, type, account)
    if str(res['code']) == 911:
        return {"result": 911}
    elif str(res['code']) == '0':
        pwd = res['password']
        phone = res.get('number', '')
        uid = res['uid']
        AMS_KEY = get_config(brandid, 'AMS_KEY')#config.SETTINGS.get(brandid, {}).get('AMS_KEY') or config.SETTINGS.get('all', {}).get('AMS_KEY', '')
        if md5(rc4(hex2str(pwd), AMS_KEY)).hexdigest() == md5pwd:
            return {"result": 0, "kcid": uid, "phone": phone}
        else:
            return {"result": 2}
    return {"result": 1}

def getInfo(brandid, account_type, account):
    uid, mobile, password, email, check = '', '', '', '', ''
    if not account or account == 'null':
        return uid, mobile, password
    if len(str(account)) == 11 and str(account)[0] == '1':
        account_type = 'mobile'
    res = info(brandid, account_type, account)
    if res['code'] == 911:
        uid = 911
    elif res['code'] == '0':
        uid = res['uid']
        mobile = res.get('number', '')
        email = res.get('email', '')
        check = res.get('check', 'false')
        AMS_KEY = get_config(brandid, 'AMS_KEY')#config.SETTINGS.get(brandid, {}).get('AMS_KEY') or config.SETTINGS.get('all', {}).get('AMS_KEY', '')
        password = rc4(hex2str(res['password']), AMS_KEY)
    return uid, password, mobile, email, check

def get_detail_info(brandid, account_type, account):
    res = {}
    if not account or account == "null" or account_type == "error":
        return res
    res = detail_info(brandid, account_type, account)
    return res

def upload_login_info(brandid, uid, pv='', v='', ptype='', netmode='', ip=''):
    ''' 上报登录信息  '''
    params = {
        'uid':uid,
        'brandid':brandid,
        'pv':pv,
        'v':v ,
        'ptype':utf8(ptype),
        'netmode':netmode,
        'ip':ip,
    }
    encode_params = urllib.urlencode(params)
    res = getAmsResp(brandid, 'logininforep.act', encode_params)
    return res
    #logging.info('登录上报结果 %s params %s', res, params)

def mobileregvalidate(brandid, number, type='', ip=''):
    '''获取验证码'''
    params = {
        'brandid':brandid,
        'number':number,
        'type':type,
        'ip':ip,
    }
    encode_params = urllib.urlencode(params)
    res = getAmsResp(brandid, 'mobileregvalidate.act', encode_params)
    return res

def mobileregsubmitnopwd(brandid, number, verifyCode, invitedby, invitedflag, regfrom, ip, platform, pv, v, phone_model, ext=''):
    '''提交验证码注册'''
    params = {
                "brandid": brandid,
                "number": number,
                "verifyCode":verifyCode,
                "invitedby": invitedby,
                "invitedflag": invitedflag,
                "from": regfrom,
                "ip": ip,
                "pform":platform,
                "psystem":pv,
                "cversion":v,
                "ptype":utf8(phone_model),
                "ext": ext,
                }

    encode_params = urllib.urlencode(params)
    res = getAmsResp(brandid, 'mobileregsubmitnopwd.act', encode_params)
    return res

if __name__ == '__main__':
    #print getInfo('feiin','mobile','13760145290')
    print upload_login_info('2', 'kc', '127.0.0.1', 'dd', 'd2', 'fjkdas', '3g')

