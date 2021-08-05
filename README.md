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
  'now_address' : '1',            # 当前所在地：内地
    'gps_now_address': '',            #
    'now_province': '340000',        # 当前所在地：安徽
    'gps_province': '',                #
    'now_city': '340100',            # 当前所在地：合肥
    'gps_city': '',                    #
    'now_detail': '',                #
    'is_inschool': '6',                # 是否在校：西校区
    'body_condition':    '1',        # 当前身体状况：正常
    'body_condition_detail': '',    #
    'now_status': '1',                # 当前状态：正常在校园内
    'now_status_detail': '',        #
    'has_fever': '0',                # 当前有无发热症状：无
    'last_touch_sars': '0',            # 有无接触患者：无
    'last_touch_sars_date': '',        #
    'last_touch_sars_detail': '',    #
    'last_touch_hubei': '0',        # 有无接触湖北人员：无
    'last_touch_hubei_date': '',    #
    'last_touch_hubei_detail': '',    #
    'last_cross_hubei': '0',        # 有无在湖北停留或路过：无
    'last_cross_sars_date': '',        #
    'last_cross_sars_detail': '',    #
    'return_dest': '1',                # 返校目的地：合肥校本部
    'return_dest_detail': '',        #
    'other_detail': '',                # 其他情况说明：（无）
}

```

## Requirements
```
pip install lxml requests
```

## Run
```
bash run.sh
```
or
```
python3 reporter.py $USERNAME $PASSWORD $MAIL_USER $MAIL_PASS $MAIL_TARGET $LOCATION
```
