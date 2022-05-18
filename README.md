# USTC-COVID-Reporter

[https://weixine.ustc.edu.cn/2020/home](https://weixine.ustc.edu.cn/2020/home)  you can deploy it with `crontab` to report automatically.

## configuration

Edit your identify information and mail configuration

```python
USERNAME = 'SA19000000' # your unified identity authentication ID
PASSWORD = '123456' # your unified identity authentication PASSWORD
MAIL_USER = 'zhangsan@mail.ustc.edu.cn' # the mail you want to use it to send email (only recommend your ustc mail, if not please make sure your mail host is right in sendEmail.py )
MAIL_PASS = '123456' # the mail pass  you want to use it to send email
MAIL_TARGET = 'zhansan@foxmail.com' # the mail your want receive email
LOCATION = 1 # 1 means 安徽 2 means 江苏
```

Edit `reporter.py` to configure your report information

```python
report_payload = {
  '_token': token,                # 加入上面获得的token
  'juzhudi': "先研院",
  'body_condition': '1',
  'body_condition_detail':'' ,
  'now_status': '1',
  'now_status_detail': '',
  'has_fever': '0',
  'last_touch_sars': '0',
  'last_touch_sars_date': '',
  'last_touch_sars_detail': '',
  'is_danger': '0',
  'is_goto_danger': '0',
  'jinji_lxr': 'xxx',
  'jinji_guanxi': '父亲',
  'jiji_mobile': 'phone_number',
  'other_detail': ''
}

```

## Requirements
```
pip install lxml requests
```

## Run
```
python3 reporter.py $USERNAME $PASSWORD $MAIL_USER $MAIL_PASS $MAIL_TARGET $LOCATION $LOCATION
```

## Use github action schedule function
edit it in .github/workflow/python-app.yml
```
schedule:
	- cron '0 0 * * *'
```
also remember to add `action secrets` in project
```
LOCATION
TARGET_MAIL_USER
USTC_MAIL_PASS
USTC_MAIL_USER
USTC_PASS
USTC_USER
```

## Use serverless function to trigger github dispatch (perform daily task automatically)
Serverless Function
```
# -*- coding: utf8 -*-
import requests
import json

def trigger_ustc_covid19reporter():
        payload = json.dumps({"event_type": "run"})
        print("start to run")
        header = {"Authorization": "token ${token}",
                  "Accept": "application/vnd.github.everest-preview+json"}
        response_decoded_json = requests.post(
                f'https://api.github.com/repos/ZacharyLiu-CS/USTC-COVID-Reporter/dispatches',
            data=payload, headers=header)
```
