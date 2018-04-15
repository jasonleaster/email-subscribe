# !/usr/bin/env python
# coding=utf-8

import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests

GIRL, BOY = "广州", "肇庆"
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

MAIL_HOST = os.environ.get("MAIL_HOST")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
WEATHER_KEY = os.environ.get("WEATHER_KEY")

RECEIVER = ["1259462438@qq.com"]
SENDER = "chenjiandongx@qq.com"

# 聚合数据天气预报 api
weather_api = "https://www.sojson.com/open/api/weather/json.shtml?city={}"


def get_weather_info():
    """
    获取天气信息
    """
    girl = requests.get(weather_api.format(GIRL, headers=HEADERS)).json()
    boy = requests.get(weather_api.format(BOY, headers=HEADERS)).json()

    girl_today = girl["data"]["forecast"][0]
    girl_tomorrow = girl["data"]["forecast"][1]
    boy_tomorrow = boy["data"]["forecast"][1]

    if girl and boy:
        content = (
            "你好，傻宝宝:\n\n\t"
            "今天是 {_today}，{_week}。\n\t"
            "首先，今天已经是我们相恋的第 {loving_days} 天了喔。然后我就要来播送天气预报了！！\n\n\t"
            "广州明天{_g_tomorrow_high}，{_g_tomorrow_low}，天气 {_g_tomorrow_type}，"
            "需要注意的是{_g_tomorrow_notice}\n\n\t"
            "肇庆明天{_b_tomorrow_high}，{_b_tomorrow_low}，天气 {_b_tomorrow_type}，"
            "需要注意的是{_b_tomorrow_notice}"
        )
        return content.format(
            loving_days=get_loving_days(),
            _today=get_today(girl["date"]),
            _week=girl_today["date"][-3:],
            _g_tomorrow_high=girl_tomorrow["high"],
            _g_tomorrow_low=girl_tomorrow["low"],
            _g_tomorrow_type=girl_tomorrow["type"],
            _g_tomorrow_notice=girl_tomorrow["notice"],
            _b_tomorrow_high=boy_tomorrow["high"],
            _b_tomorrow_low=boy_tomorrow["low"],
            _b_tomorrow_type=boy_tomorrow["type"],
            _b_tomorrow_notice=boy_tomorrow["notice"],
        )


def get_loving_days():
    """
    获取恋爱天数
    """
    today = datetime.datetime.today()
    anniversary = datetime.datetime(2015, 7, 2)
    return (today - anniversary).days


def get_today(today):
    """
    格式化今天日期
    """
    return "{}-{}-{}".format(today[:4], today[4:6], today[6:])


def send_email():
    """
    发送邮件
    """
    try:
        content = get_weather_info()
    except Exception:
        try:
            content = get_weather_info()
        except Exception:
            content = "傻宝宝，这傻逼接口他妈的又挂了喔！"
    message = MIMEText(content, "plain", "utf-8")
    message["From"] = Header("暖宝宝", "utf-8")
    message["To"] = Header("a handsome soul")
    message["Subject"] = Header("男朋友的日常问候", "utf-8")
    try:
        smtp_obj = smtplib.SMTP_SSL(MAIL_HOST)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(SENDER, RECEIVER, message.as_string())
        smtp_obj.quit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    send_email()
