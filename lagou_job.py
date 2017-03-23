# -*- coding=utf-8 -*-
import requests
from lxml import html
import urllib
import json


'''
拉钩的抓取，首先找到最后的post，带上全部的cookies可以拿到，否则404页
通过逆向，一步步找到所需cookies，完成。
'''

# headers = {
#     'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0;\
#     Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)'
# }
#
# cookies = {
#     '_ga': 'GA1.2.2003702965.1486066203',
#     '_gat': '1',
#     'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1486066567',
#     'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1486066203',
#     'index_location': '',
#     'JSESSIONID': '99021FFD6F8EC6B6CD209754427DEA93',
#     'LGUID': '20170203041008-9835b1c9-e983-11e6-8a36-525400f775ce',
#     'LGSID': '20170203041008-9835b03a-e983-11e6-8a36-525400f775ce',
#     'LGRID': '20170203041612-714b1ea3-e984-11e6-8a36-525400f775ce',
#     'PRE_HOST': '',
#     'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F',
#     'PRE_SITE': '',
#     'PRE_UTM': '',
#     'SEARCH_ID': 'bfed7faa3a0244cc8dc1bb361f0e8e35',
#     'user_trace_token': '20170203041008-9835aec2-e983-11e6-8a36-525400f775ce',
# }
#
# post_url = 'https://www.lagou.com/jobs/positionAjax.json'
#
# post_data = {
#     'first': 'true',
#     'pn': '1',
#     'kd': 'Python'
# }
#
# resp = requests.post(url=post_url, data=post_data, headers=headers, cookies=cookies)
# print(resp.content)


headers = {
    'user-agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0;\
    Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)'
}

s = requests.session()
r = s.get('http://www.lagou.com')
cookies = {
    'JSESSIONID': r.cookies['JSESSIONID']  # 得到cookies的一项, JSESSIONID
}
r = s.get('https://a.lagou.com/collect?v=1&_v=j31&a=111842258&t=pageview&_s=1&dl=https%3A%2F%2Fwww.lagou.com%2F&ul= \
          zh-cn&de=UTF-8&dt=%E6%8B%89%E5%8B%BE%E7%BD%91-%E6%9C%80%E4%B8%93%E4%B8%9A%E7%9A%84%E4%BA%92%E8%81%94%E7%B \
          D%91%E6%8B%9B%E8%81%98%E5%B9%B3%E5%8F%B0_%E6%89%BE%E5%B7%A5%E4%BD%9C_%E6%8B%9B%E8%81%98_%E4%BA%BA%E6%89%8D \
          %E7%BD%91_%E6%B1%82%E8%81%8C&sd=24-bit&sr=1366x768&vp=1349x213&je=0&fl=24.0%20r0&_u=MACAAAQBK~&jid=&cid=18 \
          9619300.1490148377&tid=UA-41268416-1&z=1935926164')
# 'https://a.lagou.com/collect?v=1&_v=j31&a=111842258&t=pageview&_s=1&dl=https://www.lagou.com/&ul=zh-cn&de=UTF-8& \
# dt=拉勾网-最专业的互联网招聘平台_找工作_招聘_人才网_求职&sd=24-bit&sr=1366x768&vp=1349x213&je=0&fl=24.0 r0&_u=MA \
# CAAAQBK~&jid=&cid=189619300.1490148377&tid=UA-41268416-1&z=1935926164'
# query_string = {
#     'v': '1',
#     't': 'a',
#     'dl': 'https://www.lagou.com/',
#     'dr': 'https://www.lagou.com/',
#     'dt': '拉勾网-最专业的互联网招聘平台_找工作_招聘_人才网_求职',
#     'aid': '4O00_0102_0_idnull_1196',
#     'intrack': 'index_navigation'
# }

cookies.update(r.cookies.get_dict())  # 得到cookies的多项,

r = s.get('https://www.lagou.com/zhaopin/Python/?labelWords=label')  # 得打cookies的一项，SEARCHID
cookies.update(r.cookies.get_dict())

post_url = 'https://www.lagou.com/jobs/positionAjax.json'

post_data = {
    'first': 'true',
    'pn': '1',
    'kd': 'Python'
}
resp = s.post(url=post_url, data=post_data, headers=headers, cookies=cookies)
null, true, false = '', 'true', 'false'
resp = eval(resp.content)  #  text->str, content->bytes, eval实现str->dict

contents = resp['content']['hrInfoMap']  # positionId
infos = resp['content']['positionResult']['result']

'''
{
    "success": true,
    "requestId": null,
    "resubmitToken": null,
    "msg": null,
    "content": {
        "pageNo": 1,
        "pageSize": 15,
        "hrInfoMap": {
            "2714158": {
                "userId": 93804,
                "phone": null,
                "positionName": "Hr",
                "receiveEmail": null,
                "realName": "hr",
                "portrait": "image1/M00/33/7C/CgYXBlWTqdSAI6VoAACAXLWZoT0216.jpg",
                "canTalk": true,
                "userLevel": "G1"
            },
            "2846934": {
                "userId": 7034992,
                "phone": null,
                "positionName": "",
                "receiveEmail": null,
                "realName": "davidcui",
                "portrait": null,
                "canTalk": true,
                "userLevel": "G1"
            }
        },
        "positionResult": {
            "locationInfo": {
                "city": null,
                "district": null,
                "queryByGisCode": false,
                "businessZone": null,
                "locationCode": null
            },
            "queryAnalysisInfo": {
                "positionName": "python",
                "companyName": null,
                "industryName": null,
                "usefulCompany": false
            },
            "strategyProperty": {
                "name": "dm-csearch-default",
                "id": 0
            },
            "resultSize": 15,
            "totalCount": 1178,
            "result": [
                {
                    "lastLogin": 1490148152000,
                    "publisherId": 7034992,
                    "explain": null,
                    "plus": null,
                    "pcShow": 0,
                    "appShow": 0,
                    "deliver": 0,
                    "gradeDescription": null,
                    "promotionScoreExplain": null,
                    "firstType": "\xe5\xbc\x80\xe5\x8f\x91/\xe6\xb5\x8b\xe8\xaf\x95/\xe8\xbf\x90\xe7\xbb\xb4\xe7\xb1\xbb",
                    "secondType": "\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xbc\x80\xe5\x8f\x91",
                    "positionLables": [
                        "\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xbc\x80\xe5\x8f\x91",
                        "linux",
                        "\xe7\x9b\x91\xe6\x8e\xa7",
                        "python"
                    ],
                    "businessZones": [
                        "\xe5\xa4\xa9\xe6\xb2\xb3\xe5\x85\xac\xe5\x9b\xad",
                        "\xe4\xb8\x9c\xe5\x9c\x83",
                        "\xe6\xa3\xa0\xe4\xb8\x8b"
                    ],
                    "imState": "disabled",
                    "companyFullName": "\xe4\xbc\x98\xe7\xbb\xb4\xe7\xa7\x91\xe6\x8a\x80\xef\xbc\x88\xe6\xb7\xb1\xe5\x9c\xb3\xef\xbc\x89\xe6\x9c\x89\xe9\x99\x90\xe5\x85\xac\xe5\x8f\xb8",
                    "adWord": 0,
                    "companyId": 105373,
                    "companyShortName": "\xe4\xbc\x98\xe7\xbb\xb4\xe7\xa7\x91\xe6\x8a\x80",
                    "positionId": 2846934,
                    "industryField": "\xe7\xa7\xbb\xe5\x8a\xa8\xe4\xba\x92\xe8\x81\x94\xe7\xbd\x91,\xe4\xbc\x81\xe4\xb8\x9a\xe6\x9c\x8d\xe5\x8a\xa1",
                    "education": "\xe6\x9c\xac\xe7\xa7\x91",
                    "workYear": "1-3\xe5\xb9\xb4",
                    "city": "\xe5\xb9\xbf\xe5\xb7\x9e",
                    "positionAdvantage": "\xe7\x89\x9b\xe4\xba\xba\xe5\xb8\xa6\xe9\x98\x9f,DevOp,A\xe8\xbd\xae,\xe6\x9c\x9f\xe6\x9d\x83",
                    "createTime": "2017-03-06 13:04:40",
                    "salary": "8k-15k",
                    "positionName": "Python\xe5\xbc\x80\xe5\x8f\x91\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xb8\x88",
                    "companySize": "15-50\xe4\xba\xba",
                    "companyLogo": "i/image/M00/0E/00/Cgp3O1barriAEqo_AABQDBHZEKc257.png",
                    "financeStage": "\xe6\x88\x90\xe9\x95\xbf\xe5\x9e\x8b(A\xe8\xbd\xae)",
                    "approve": 1,
                    "jobNature": "\xe5\x85\xa8\xe8\x81\x8c",
                    "district": "\xe5\xa4\xa9\xe6\xb2\xb3\xe5\x8c\xba",
                    "companyLabelList": [
                        "\xe5\xb9\xb4\xe5\xba\x95\xe5\x8f\x8c\xe8\x96\xaa",
                        "\xe5\x8d\x88\xe9\xa4\x90\xe8\xa1\xa5\xe5\x8a\xa9",
                        "\xe8\x82\xa1\xe7\xa5\xa8\xe6\x9c\x9f\xe6\x9d\x83",
                        "\xe5\xbc\xb9\xe6\x80\xa7\xe5\xb7\xa5\xe4\xbd\x9c"
                    ],
                    "score": 0,
                    "formatCreateTime": "2017-03-06"
                }
            ]
        }
    },
    "code": 0
}'
'''

for info in infos:
    publisherId, firstType = info['publisherId'], info['firstType']
    secondType, positionLabes = info['secondType'], info['positionLables']
    businessZone, companyFullName = info['businessZones'], info['companyFullName']
    companyShortName, industryField = info['companyShortName'], info['industryField']
    education, workYear, city = info['education'], info['workYear'], info['city']
    createTime, salary = info['createTime'], info['salary']

    print(publisherId, firstType, secondType, positionLabes, businessZone, companyFullName, \
          companyShortName, industryField, education, workYear, city, salary, createTime)
