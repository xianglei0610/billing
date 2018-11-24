# -*- coding: utf-8 -*-

def set_lib_path():
    import sys
    import os
    sys.path.append('../libs')
set_lib_path()

import requests


IP = '127.0.0.1'
PORT = '8223'

root_url = 'http://%s:%s'%(IP, PORT)

def Test_precall_notify():
    payload = {
        'caller': '106861135',
        'appid': 'dare45646fewqefa',
        'calltype':'0',
        'called': '008618627002629'
    }
    
    r = requests.get(root_url + '/api/precall_notify/',params=payload)
    assert 200 == r.status_code
    print 'GET result:',r.text
    
def Test_called_notify():
    payload = {
        'caller': '106861135',
        'appid': 'dare45646fewqefa',
        'calltype': '0',
        'called': '008618627002629',
        'callid': '7258225',
        'starttime': '2014-06-20 17:00:00',
        'stoptime': '2014-06-20 17:03:00',
        'length': 681
    }
    
    r = requests.get(root_url + '/api/called_notify/',params=payload)
    assert 200 == r.status_code
    print 'GET result:',r.text