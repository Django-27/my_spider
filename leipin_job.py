# -*- coding=utf-8 -*-
import requests
from lxml import html
import logging
from wxpy import get_wechat_logger

class Liepin(object):
    name = 'liepin'

    def start_request(self, param):
        city = param.get('city_id', '010')
        query = param.get('query', 'python')
        page = param.get('page', '1')
        page = int(page) - 1

        # 筛选条件：北京，python，页数
        url = 'https://www.liepin.com/zhaopin/?industries=&dqs=010&salary=' \
              '&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1' \
              '&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=1&' \
              'fromSearchBtn=2&headckid=518ac92d9ad2dbd9&key=python'.format(city, query, page)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0'
        }

        # 重试三次的抓取
        for i in range(3):
            r = self.request(url, headers)
            if r is not None and r.status_code == 200 and r.ok:
                return self.parse_data(r, param)
            else:
                pass

    def request(self, url, headers):
        try:
            r = requests.get(url=url, headers=headers, timeout=20)
            return r
        except Exception as e:
            pass

    def parse_data(self, r, param):
        jobs_list = []
        try:
            dom = html.fromstring(r.content)
            for job in dom.xpath('//div/ul[@class="sojob-list"]/li'):
                try:
                    job_name = job.xpath('.//div[@class="job-info"]//a/text()')[0].strip()
                    job_name_url = job.xpath('.//div[@class="job-info"]//a/@href')[0]
                    job_condition = job.xpath('.//div[@class="job-info"]//p[@class="condition clearfix"]/@title')[0]
                    company_name = job.xpath('.//p[@class="company-name"]/a/@title')[0]
                    company_name_url = job.xpath('.//p[@class="company-name"]/a/@href')[0]
                    company_info = job.xpath('.//a[@class="industry-link"]/text()')[0]
                    others = job.xpath('.//p[@class="temptation clearfix"]/span/text()')
                    jobs_list.append([job_name, job_condition, company_name, company_info, others, job_name_url, company_name_url])

                except Exception as e:
                    print('liepin parse job exception')
        except Exception as e:
            print('liepin parse jobs exception')
        print(str(jobs_list))

if __name__ == '__main__':
    logger_msg = get_wechat_logger()
    liepin = Liepin()
    logger_msg.warn(liepin.start_request(param={}))
