# -*- coding -*-
import requests
import time
import cv2


def get_captcha_1(data):
    with open('captcha.gif', 'wb') as fp:
        fp.write(data)
    img = cv2.imread('captcha.jpg')
    cv2.imshow('验证码', img)
    cv2.waitKey(5)
    return input("输入验证码：")


def login(phone_num, password):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    }
    session = requests.Session()
    resp = session.get('https://www.zhihu.com/#signin', headers=headers)
    xsrf = resp.cookies['_xsrf']

    resp = session.get('https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time()*1000), headers=headers)  # 拿到验证码

    data = {
        '_xsrf': xsrf,
        'password': password,
        'captcha': get_captcha_1(resp.content),
        'phone_num': phone_num
    }

    resp = session.post('https://www.zhihu.com/login/phone_num', data=data, headers=headers)  # 登录成功
    print(eval(resp.content)['msg'])

if __name__ == '__main__':
    login('18614035475', '147850096')
















