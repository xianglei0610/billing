def set_lib_path():
    import sys
    import os
    sys.path.append('../libs')
set_lib_path() 

def test_type():
    from XML2Dict import XML2Dict
    xml = XML2Dict()
    file = open('sample.xml')
    r = xml.parse(file.read())
    print r
    print r.get('me')
    
def test_request_paras():
    from XML2Dict import XML2Dict
    xml = XML2Dict()
    file = open('request_body.xml')
    r = xml.parse(file.read())
    print r