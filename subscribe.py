import os

import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

import requests


weather_api = "http://v.juhe.cn/weather/index?format=2&" \
              "cityname={cityname}&key={key}"


def get_weather_info():
    """

    :return:
    """
    _guangzhou = "广州"
    _zhaoqing = "肇庆"
    _weather_key = os.environ.get('WEATHER_KEY')

    req = requests.get(
        weather_api.format(cityname=_guangzhou, key=_weather_key)).json()

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
    _mail_host= os.environ.get('MAIL_HOST')
    _mail_user = os.environ.get('MAIL_USER')
    _mail_pass = os.environ.get('MAIL_PASS')
    _receiver = [os.environ.get('RECEIVER')]
    _sender = 'chenjiandongx@qq.com'

    content = get_weather_info()

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('A handsome boy', 'utf-8')
    message['To'] = Header('A beautiful girl')
    message['Subject'] = Header('日常关心', 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(_mail_host)
        smtpObj.login(_mail_user, _mail_pass)
        smtpObj.sendmail(_sender, _receiver, message.as_string())
        smtpObj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()