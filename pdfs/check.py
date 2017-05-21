import re


def match(data):
    phone = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    if not phone.match(data['contact']):
        return "phone not match"
    try:
        peoplenumber = int(data['people'])
        if peoplenumber < 1 or peoplenumber > 200:
            return "people number wrong"
    except ValueError:
        return "people not integer"
    usernamelen = len(data['username'])
    if usernamelen > 20:
        return "username too long"
    titlelen = len(data['title'])
    if titlelen > 20:
        return "title too long"
    # desclen = len(data['desc'])
    utf8desxlen = len(data['desc'].encode('utf-8'))
    # print ("len:", desclen, utf8desxlen)
    if utf8desxlen > 700:
        return "desc too long"
    utf8additionallen = len(data['additional'].encode('utf-8'))
    # print(utf8additionallen)
    if utf8additionallen > 217:
        return "additional too long"
    return False
