import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

import requests

GUANGZHOU = "广州"
ZHAOQING = "肇庆"

MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
RECEIVERS = [os.environ.get("RECEIVER")]
WEATHER_KEY = os.environ.get("WEATHER_KEY")

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

    content = "温度：{temperature}，天气为：{weather}".format(
        temperature=today['temperature'],
        weather=today['weather']
    )
    return content


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
    message['From'] = Header('A handsome boy', 'utf-8')
    message['To'] = Header('A beautiful girl')
    message['Subject'] = Header('日常关心', 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(MAIL_HOST)
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(SENDER, RECEIVERS, message.as_string())
        smtpObj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()
