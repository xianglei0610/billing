#!python
# -*- coding:utf-8 -*-
'''
公用函数(rc4加密)
Created on 2014/5/26
@author: Holer
'''
import xstr

__all__ = ("decode", 'encode')

def RC4(data, key):
    '''rc4加密的核心算法'''
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

def decode(rc4_txt, key, **kwargs):
    '''将rc4加密后的密文，解密出来
    @param {string} rc4_txt RC4加密后的密文
    @param {string} key 加密/解密的key值
    @return {string} 返回解密后的明文
    '''
    rc4_txt = xstr.to_str(rc4_txt)
    key = xstr.to_str(key)
    real_text = RC4(hex2str(rc4_txt), key)
    return real_text

def encode(real_text, key, **kwargs):
    '''将明文字符串，用RC4加密成密文
    @param {string} real_text 明文的字符串
    @param {string} key 加密/解密的key值
    @return {string} 返回加密后的密文
    '''
    real_text = xstr.to_str(real_text)
    key = xstr.to_str(key)
    rc4_txt = str2hex(RC4(real_text, key))
    return rc4_txt
