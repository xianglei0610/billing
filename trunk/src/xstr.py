#!python
# -*- coding:utf-8 -*-
'''
公用函数(字符串处理)
Created on 2014/7/16
@author: Holer
'''
import re
import sys
import time
import datetime
import json

__all__=('to_unicode', 'to_str', 'to_human', 'to_json', 'json2str', 'mod', 'to_html', 'to_text', 'remove_htmlTag')

def to_unicode(value, all2str=False, to_human=False, from_code=None, **kwargs):
    """将字符转为 unicode 编码
    @param {任意} value 将要被转码的值,类型可以是:str,unicode,int,long,float,double,dict,list,tuple,set,其它类型
    @param {boolean} all2str 是否要将数值、日期、布尔等类型也转成字符串,(list,tuple,set,dict等类型会保持不变,只转换里面的值)
    @param {boolean} to_human 是否要将字符串转码成便于人阅读的编码(将 “\u65f6”,“\xE5\x8C\x85”等字符转为人可以阅读的文字)
    @param {string} from_code 传入字符串的可能编码类型,如果有则优先按它解码
    @return {unicode|type(value)} 返回转成 unicode 的字符串,或者原本的参数类型
    """
    if value == None:
        return u'' if all2str else None
    # str/unicode 类型的
    elif isinstance(value, basestring):
        # str类型,需要按它原本的编码来解码出 unicode,编码不对会报异常
        if isinstance(value, str):
            for encoding in (from_code, "utf-8", "gbk", "big5", sys.getdefaultencoding(), "cp936", "latin-1", "ascii"):
                if not encoding or not isinstance(encoding, basestring): continue
                try:
                    value = value.decode(encoding)
                    break # 如果上面这句执行没报异常，说明是这种编码
                except:
                    pass
        # 上面已经转码成 Unicode 的
        if to_human and value:
            try:
                # eval 处理是为了让“\u65f6”,“\xE5\x8C\x85”等字符转为人可以阅读的文字
                if "'''" not in value:
                    value = eval(u"u'''%s'''" % value)
                elif '"""' not in value:
                    value = eval(u'u"""%s"""' % value)
                else:
                    value = json.dumps(value, ensure_ascii=False)
                    value = value.replace(r"\\u", r"\u") # json.dumps 会转换“\”,使得“\u65f6”变成“\\u65f6”
                    value = eval(u'u%s' % value)
            except:
                pass
        return value
    # 考虑是否需要转成字符串的类型
    elif isinstance(value, (bool,int,long,float,complex)):
        return unicode(value) if all2str else value
    # time 类型转成字符串,需要写格式
    elif isinstance(value, time.struct_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', value) if all2str else value
    # datetime 类型转成字符串,需要写格式
    elif isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S') if all2str else value
    # list,tuple,set 类型,递归转换
    elif isinstance(value, (list,tuple,set)):
        arr = [to_unicode(item, all2str=all2str, to_human=to_human, from_code=from_code, **kwargs) for item in value]
        # 尽量不改变原类型
        if isinstance(value, list):  return arr
        if isinstance(value, tuple): return tuple(arr)
        if isinstance(value, set):   return set(arr)
    # dict 类型,递归转换(字典里面的 key 也会转成 unicode 编码)
    elif isinstance(value, dict):
        this_value = {} # 不能改变原参数
        for key1,value1 in value.items():
            # 字典里面的 key 也转成 utf8 编码
            if isinstance(key1, str):
                key1 = to_unicode(key1, all2str=all2str, to_human=to_human, from_code=from_code, **kwargs)
            this_value[key1] = to_unicode(value1, all2str=all2str, to_human=to_human, from_code=from_code, **kwargs)
        return this_value
    # 其它类型
    else:
        value = unicode(value) if all2str else value
        return value


def to_str(value, all2str=False, encode="utf-8", **kwargs):
    """将字符转为utf8编码
    @param {任意} value 将要被转码的值,类型可以是:str,unicode,int,long,float,double,dict,list,tuple,set,其它类型
    @param {string} encode 编码类型,默认是 utf-8 编码
    @param {boolean} all2str 是否要将数值类型、日期类型、布尔类型等类型也转成字符串,(list,tuple,set,dict等类型会保持不变,只转换里面的值)
    @param {boolean} to_human 是否要将字符串转码成便于人阅读的编码(将 “\u65f6”,“\xE5\x8C\x85”等字符转为人可以阅读的文字)
    @param {string} from_code 传入字符串的可能编码类型,如果有则优先按它解码
    @return {str|type(value)} 返回转成 unicode 的字符串,或者原本的参数类型
    """
    # 字符串类型的,先转成 unicode,再转成 utf8 编码的 str,这样就可以避免编码错误了
    if isinstance(value, basestring):
        return to_unicode(value, all2str=all2str, **kwargs).encode(encode)
    # list,tuple,set 类型,递归转换
    elif isinstance(value, (list,tuple,set)):
        arr = [to_str(item, all2str=all2str, encode=encode, **kwargs) for item in value]
        # 尽量不改变原类型
        if isinstance(value, list):  return arr
        if isinstance(value, tuple): return tuple(arr)
        if isinstance(value, set):   return set(arr)
    # dict 类型,递归转换(字典里面的 key 也会转成 utf8 编码)
    elif isinstance(value, dict):
        this_value = {} # 不能改变原参数
        for key1,value1 in value.items():
            # 字典里面的 key 也转成 utf8 编码
            if isinstance(key1, unicode):
                key1 = to_str(key1, all2str=all2str, encode=encode, **kwargs)
            this_value[key1] = to_str(value1, all2str=all2str, encode=encode, **kwargs)
        return this_value
    # 其它类型,可以部分地交给 to_unicode 处理
    return to_unicode(value, all2str=all2str, **kwargs).encode(encode) if all2str else value


def to_human(value, isJson = False, **kwargs):
    '''将 字符串/其他值 按便于人阅读的形式展示
    类似于 repr 函数,但同时会将 “\u65f6”,“\xE5\x8C\x85”等字符转为人可以阅读的文字
    @param {任意} value 将要被转码的值,类型可以是:str,unicode,int,long,float,double,dict,list,tuple,set,其它类型
    @param {boolean} isJson: 返回结果是否需要反 json 化
    @return {unicode} 返回转成 unicode 的字符串,且呈现便于人阅读的模式
        本函数与 to_unicode(value, to_human=True) 函数的区别是: to_unicode 只转换字符串,且 (list,tuple,set, dict) 不改变类型。
        而本函数会将所有类型转成字符串,包括 (list,tuple,set, dict) 类型,且这些类型会尽量美化输出。
    '''
    # 先将可以转成字符串的都先转成字符串
    value = to_unicode(value, all2str=True, to_human=True)
    if isinstance(value, basestring):
        value = value.strip()
        # json 格式的,尽量按 json 格式美化一下输出
        if isJson or (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']')):
            value = to_json(value)
    # list,tuple,set,dict 类型,按 json 格式美化一下输出
    if isinstance(value, (list,tuple,set, dict)):
        return json.dumps(value, indent=2, ensure_ascii=False)
    # 其它类型,可以部分地交给 to_unicode 处理
    return value


def to_json(value, **kwargs):
    '''将字符串转成json
    @param {string} value 要转成json的字符串
    @return {dict} 返回转换后的类型
    '''
    if isinstance(value, basestring):
        try:
            value = json.loads(value)
        except:
            try:
                value = eval(value)
            except:
                pass
    return value


def json2str(value, **kwargs):
    '''将 dict 类型的内容转成json格式的字符串
    @param {dict} value 要转成json字符串的内容
    @return {string} 返回转换后的字符串
    '''
    try:
        value = json.dumps(value)
    except:
        pass
    return value


def mod(sour, param=None, *args, **kwargs):
    '''相当于使用“%”格式化字符串
    @param {string} sour 要格式化的字符串
    @param {任意} param 要放入字符串的参数,多个则用 tuple 括起来
    @param {boolean} to_human 是否要将字符串转码成便于人阅读的编码(将 “\u65f6”,“\xE5\x8C\x85”等字符转为人可以阅读的文字)
    @return {string} 返回格式化后的字符串(unicode编码),即返回: sour %  param
    '''
    kwargs.pop('all2str', None)
    if isinstance(sour, str):
        sour = to_str(sour, **kwargs)
        if not param:
            return sour
        return sour % to_str(param, **kwargs)
    elif isinstance(sour, unicode):
        if not param:
            return sour
        return sour % to_unicode(param, **kwargs)
    else:
        return unicode(sour)


def to_html(sour, *args, **kwargs):
    '''
    转换字符串成 Html 页面上显示的编码
    @param sour 需要转换的字符串
    @return 转换后的字符串
    @example to_html(" ") 返回: &nbsp;
    '''
    # 以下逐一转换
    sour = sour.replace("&", "&amp;")
    sour = sour.replace("%", "&#37;")
    sour = sour.replace("<", "&lt;")
    sour = sour.replace(">", "&gt;")
    sour = sour.replace("\n", "\n<br/>")
    sour = sour.replace('"', "&quot;")
    sour = sour.replace(" ", "&nbsp;")
    sour = sour.replace("'", "&#39;")
    sour = sour.replace("+", "&#43;")
    return sour


def to_text(sour, *args, **kwargs):
    '''
    转换字符串由 Html 页面上显示的编码变回正常编码(以上面的方法对应)
    @param sour 需要转换的字符串
    @return 转换后的字符串
    @example to_text("&nbsp;") 返回: " "
    '''
    # 以下逐一转换
    # 先转换百分号
    sour = sour.replace("&#37;", "%")
    # 小于号,有三种写法
    sour = sour.replace("&lt;", "<")
    sour = sour.replace("&LT;", "<")
    sour = sour.replace("&#60;", "<")
    # 大于号,有三种写法
    sour = sour.replace("&gt;", ">")
    sour = sour.replace("&GT;", ">")
    sour = sour.replace("&#62;", ">")
    # 单引号
    sour = sour.replace("&#39;", "'")
    sour = sour.replace("&#43;", "+")
    # 转换换行符号
    sour = re.sub(r'\n?<[Bb][Rr]\s*/?>\n?', '\n', sour)
    # 双引号号,有三种写法
    sour = sour.replace("&quot;", '"')
    sour = sour.replace("&QUOT;", '"')
    sour = sour.replace("&#34;", '"')
    # 空格,只有两种写法, &NBSP; 浏览器不承认
    sour = sour.replace("&nbsp;", " ")
    sour = sour.replace("&#160;", " ")
    # & 符号,最后才转换
    sour = sour.replace("&amp;", "&")
    sour = sour.replace("&AMP;", "&")
    sour = sour.replace("&#38;", "&")
    return sour


def remove_htmlTag(text, *args, **kwargs):
    '''
    清除HTML标签
    @return 清除标签后的内容
    @example remove_htmlTag("<div>haha</div>") 返回: "haha"
    '''
    # 清除注释
    text = text.replace("<!--.*-->", "")
    # 标题换行: </title> ==> 换行符
    text = re.sub(r'</[Tt][Ii][Tt][Ll][Ee]>', '\n', text)
    # 换行符换行: <br/> ==> 换行符
    text = re.sub(r'\n?<[Bb][Rr]\s*/?>\n?', '\n', text)
    # tr换行: </tr> ==> 换行符
    text = re.sub(r'</[Tt][Rr]>', '\n', text)
    # html標籤清除
    text = re.sub(r'<[^>]+>', '', text)
    # 转换字符串由 Html 页面上显示的编码变回正常编码
    text = to_text(text)
    return text.strip()

