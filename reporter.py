# -*- coding: UTF-8 -*-
import sys
import requests
from requests.cookies import RequestsCookieJar
from lxml import etree
from sendEmail import SendMessage
import time
import json

USERNAME = 'xxxxxxxxx'
PASSWORD = 'xxxxxxxxx'
MAIL_USER = 'xxxxxxxxx'
MAIL_PASS = 'xxxxxxxxx'
MAIL_TARGET = 'xxxxxxxxx'
# "1" means at anhui, 2 means at jiangsu
LOCATION = 1
succed_report = False
def main():
    # Check username and password
    global USERNAME, PASSWORD,MAIL_USER,MAIL_PASS,MAIL_TARGET,succed_report,LOCATION
    if len(sys.argv) < 6:
        exit(-1)
    elif USERNAME == 'xxxxxxxxx' and PASSWORD == 'xxxxxxxxx' and MAIL_USER == 'xxxxxxxxx' and MAIL_PASS == 'xxxxxxxxx' and MAIL_TARGET == 'xxxxxxxxx' :
        USERNAME=sys.argv[1]
        PASSWORD=sys.argv[2]
        MAIL_USER=sys.argv[3]
        MAIL_PASS=sys.argv[4]
        MAIL_TARGET=sys.argv[5]
        LOCATION=int(sys.argv[6])


    req = requests.Session()
    cookie_jar = RequestsCookieJar()

    # Get the CAS_LT
    cas_url = "https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin"
    r = req.get(cas_url)
    cas_html_data = etree.HTML(r.text)
    cas_lt_line = cas_html_data.xpath("//*[@id='CAS_LT']/@value")
    assert(len(cas_lt_line) == 1)
    cas_lt = cas_lt_line[0]
    print("CAL_LT: %s",cas_lt, flush=True)

 # Prepare for the session
    login_url = 'https://passport.ustc.edu.cn/login'
    login_payload = {
            "model": "uplogin.jsp",
            "CAS_LT": cas_lt,
            "service": "https://weixine.ustc.edu.cn/2020/caslogin",
            "warn":"",
            "showCode":"",
            "username": USERNAME,
            "password": PASSWORD,
            "button":""
            }
    # Login start
    print('Requesting for cookies from: %s' % login_url, flush=True)
    r = req.post(login_url, data=login_payload, allow_redirects=False)
    print("Login status code %s",r.status_code, flush=True)
    # Redirections
    while r.status_code in range(300, 304):
        new_location = r.headers['Location']
        print("New location %s" % new_location)
        print('Redirecting to %s' % new_location, flush=True)
        cookie_jar.update(r.cookies)
        r = req.get(new_location,cookies=cookie_jar, allow_redirects=False)

    # Finally update my cookies
    cookie_jar.update(r.cookies)
    # #print(cookie_jar.keys())

    # Get my token for later commit
    login_form_data = etree.HTML(r.text)

    token_line = login_form_data.xpath("//*[@id='daliy-report']/form/input/@value")
    print( token_line, flush=True)
    assert(len(token_line) == 1)
    token = token_line[0]

    # Close login request
    r.close()

    # Prepare for report request
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    param = {
            # 'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp,image/apng, */*; q=0.8, application/signed-exchange; v=b3; q=0.9',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache - Control': 'max-age=0',
            'Content - Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://weixine.ustc.edu.cn',
            'Referer': 'https://weixine.ustc.edu.cn/2020/home',
            'Src - Fetch - Dest': 'document',
            'Src - Fetch - Mode': 'navigate',
            'Src - Fetch - Site': 'same-origin',
            'Src - Fetch - User': '71',
            'Upgrade - Insecure - Requests': '1'
            }
    report_payload = {}
    with open ('report_data.json',mode='r',encoding='utf-8') as f:
        report_payload = json.load(f)
        for i in report_payload:
            print(i)

    if LOCATION == 1:
        report_payload['_token']=token                # 加入上面获得的token
    elif LOCATION == 2:
        report_payload['_token']=token                # 加入上面获得的token

    print(cookie_jar.items(),flush=True)
    r = req.post('https://weixine.ustc.edu.cn/2020/daliy_report',
            cookies=cookie_jar, data=report_payload, headers=headers, params=param,
            allow_redirects=False, timeout=50)
    print(report_payload, flush=True)
    # Redirections
    while r.status_code in range(300, 304):
        new_location = r.headers['Location']
        #print('Redirecting to %s' % new_location)
        cookie_jar.update(r.cookies)
        r = req.get(new_location, allow_redirects=False)
    #print('Last status code: %d' % r.status_code)
    if (r.status_code == 200):
        ret_text = r.text
        last_report_info_pos = r.text.find('上次上报时间')
        last_report_time = ret_text[last_report_info_pos:(last_report_info_pos+26)]
        message = "USTC covid-19 report successfully!, last time report :{0}".format(last_report_time)
        email_sender = SendMessage()
        email_sender.send(message,MAIL_TARGET, MAIL_USER,MAIL_PASS)
        print(last_report_time, flush=True)
        print("{} report successfully!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), flush=True)
        succed_report=True
    r.close()

if __name__ == '__main__':
    for i in range(5):
        main()
        if succed_report == True:
            print("successfully report at {0}th time".format(i+1), flush=True)
            break
        else:
            time.sleep(3)
    if succed_report == False:
        message = "USTC covid-19 report failed!"
        email_sender = SendMessage()
        email_sender.send(message,MAIL_TARGET, MAIL_USER,MAIL_PASS)
        print("{} report failed!".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),flush=True)

