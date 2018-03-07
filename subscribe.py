import os

import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

import requests

GUANGZHOU = "广州"
ZHAOQING = "肇庆"
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

MAIL_HOST = os.environ.get('MAIL_HOST')
MAIL_USER = os.environ.get('MAIL_USER')
MAIL_PASS = os.environ.get('MAIL_PASS')
WEATHER_KEY = os.environ.get('WEATHER_KEY')

RECEIVER = ['1259462438@qq.com']
SENDER = 'chenjiandongx@qq.com'

# 聚合数据天气预报 api
weather_api = "https://www.sojson.com/open/api/weather/json.shtml?city={}"


def get_weather_info():
    """ 获取天气信息
    """
    guangzhou = requests.get(weather_api.format(GUANGZHOU, headers=headers)).json()
    zhaoqing = requests.get(weather_api.format(ZHAOQING, headers=headers)).json()

    if guangzhou['status'] == 200 and zhaoqing['status'] == 200:
        guangzhou_today = guangzhou['data']['forecast'][0]
        guangzhou_tomorrow=guangzhou['data']['forecast'][1]

        zhaoqing_today = zhaoqing['data']['forecast'][0]
        zhaoqing_tomorrow = zhaoqing['data']['forecast'][1]

        if guangzhou and zhaoqing:
            content = (
                "你好，傻宝宝:\n\n\t"
                "今天是 {_today}，{_week}。\n\t"
                "首先，今天已经是我们相恋的第 {loving_days} 天了喔。然后我就要来播送天气预报了！！\n\n\t"
                "广州今天{_g_today_high}，{_g_today_low}，天气 {_g_today_type}，"
                "需要注意的是{_g_today_notice}\n\t"
                "广州明天{_g_tomorrow_high}，{_g_tomorrow_low}，天气 {_g_tomorrow_type}，"
                "需要注意的是{_g_tomorrow_notice}\n\n\t"
                "肇庆今天{_z_today_high}，{_z_today_low}，天气 {_z_today_type}，"
                "需要注意的是{_z_today_notice}\n\t"
                "肇庆明天{_z_tomorrow_high}，{_z_tomorrow_low}，天气 {_z_tomorrow_type}，"
                "需要注意的是{_z_tomorrow_notice}")
            return content.format(
                loving_days=get_loving_days(),
                _today=get_today(guangzhou['date']),
                _week=guangzhou_today['date'][-3:],
                _g_today_high=guangzhou_today['high'],
                _g_today_low=guangzhou_today['low'],
                _g_today_type=guangzhou_today['type'],
                _g_today_notice=guangzhou_today['notice'],
                _g_tomorrow_high=guangzhou_tomorrow['high'],
                _g_tomorrow_low=guangzhou_tomorrow['low'],
                _g_tomorrow_type=guangzhou_tomorrow['type'],
                _g_tomorrow_notice=guangzhou_tomorrow['notice'],
                _z_today_high=zhaoqing_today['high'],
                _z_today_low=zhaoqing_today['low'],
                _z_today_type=zhaoqing_today['type'],
                _z_today_notice=zhaoqing_today['notice'],
                _z_tomorrow_high=zhaoqing_tomorrow['high'],
                _z_tomorrow_low=zhaoqing_tomorrow['low'],
                _z_tomorrow_type=zhaoqing_tomorrow['type'],
                _z_tomorrow_notice=zhaoqing_tomorrow['notice'],
            )


def get_loving_days():
    """ 获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(2015, 7, 2)
    return (today - anniversary).days


def get_today(today):
    return "{}-{}-{}".format(today[:4], today[4:6], today[6:])


def send_email():
    """ 发送邮件
    """
    content = get_weather_info()
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('暖宝宝', 'utf-8')
    message['To'] = Header('a handsome soul')
    message['Subject'] = Header('男朋友的日常问候', 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(MAIL_HOST)
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(SENDER, RECEIVER, message.as_string())
        smtpObj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print(get_weather_info())
    # send_email()
