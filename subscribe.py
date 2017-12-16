import os

import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

import requests

GUANGZHOU = "广州"
ZHAOQING = "肇庆"

MAIL_HOST = os.environ.get('MAIL_HOST')
MAIL_USER = os.environ.get('MAIL_USER')
MAIL_PASS = os.environ.get('MAIL_PASS')
WEATHER_KEY = os.environ.get('WEATHER_KEY')

RECEIVER = ['1259462438@qq.com']
SENDER = 'chenjiandongx@qq.com'

# 聚合数据天气预报 api
weather_api = "http://v.juhe.cn/weather/index?format=2&" \
              "cityname={cityname}&key={key}"


def get_weather_info():
    """ 获取天气信息
    """
    guangzhou = requests.get(
        weather_api.format(cityname=GUANGZHOU, key=WEATHER_KEY)).json()

    zhaoqing = requests.get(
        weather_api.format(cityname=ZHAOQING, key=WEATHER_KEY)).json()

    _guangzhou = guangzhou['result']['today']
    _zhaoqing = zhaoqing['result']['today']

    if _guangzhou and _zhaoqing:
        content = "傻宝宝你好:\n\t" \
                  "今天是{date_y}，{week}，是我们相恋的第 {loving_days} 天。\n\t" \
                  "广州今天{g_weather}，{g_wind}，气温 {g_temperature}，" \
                  "感觉{g_dressing_index}，{g_dressing_advice}\n\t" \
                  "肇庆今天{z_weather}，{z_wind}，气温 {z_temperature}，" \
                  "感觉{z_dressing_index}，{z_dressing_advice}"
        return content.format(
            date_y=_guangzhou['date_y'],
            week=_guangzhou['week'],
            loving_days=get_loving_days(),
            g_weather=_guangzhou['weather'],
            g_wind=_guangzhou['wind'],
            g_temperature=_guangzhou['temperature'],
            g_dressing_index=_guangzhou['dressing_index'],
            g_dressing_advice=_guangzhou['dressing_advice'],
            z_weather=_zhaoqing['weather'],
            z_wind=_zhaoqing['wind'],
            z_temperature=_zhaoqing['temperature'],
            z_dressing_index=_zhaoqing['dressing_index'],
            z_dressing_advice=_zhaoqing['dressing_advice']
        )


def get_loving_days():
    """ 获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(2015, 7, 2)
    return (today - anniversary).days


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
    send_email()
