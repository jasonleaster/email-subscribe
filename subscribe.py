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

RECEIVERS = [].append(os.environ.get('RECEIVER'))
SENDER = 'chenjiandongx@qq.com'


weather_api = "http://v.juhe.cn/weather/index?format=2&" \
              "cityname={cityname}&key={key}"


def get_weather_info():
    """

    :return:
    """
    req = requests.get(
        weather_api.format(cityname=GUANGZHOU, key=WEATHER_KEY)).json()

    today = req['result']['today']
    if today:

        content = "傻宝宝你好:\n\n  " \
                  "今天是{date_y}，{week},是我们相恋的第{loving_days}天，" \
                  "广州今天{weather}，{wind}，气温{temperature}，" \
                  "感觉{dressing_index}，{dressing_advice}。"
        return content.format(
            date_y=today['date_y'],
            week=today['week'],
            loving_days=get_loving_days(),
            weather=today['weather'],
            wind=today['wind'],
            temperature=today['temperature'],
            dressing_index=today['dressing_index'],
            dressing_advice=today['dressing_advice']
        )


def get_loving_days():
    """

    :return:
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(2015, 7, 2)
    return (today - anniversary).days


def send_email():
    """

    :return:
    """
    content = get_weather_info()
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('暖宝宝', 'utf-8')
    message['To'] = Header('傻宝宝')
    message['Subject'] = Header('来自暖宝宝的日常问候', 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(MAIL_HOST)
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(SENDER, RECEIVERS, message.as_string())
        smtpObj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()
