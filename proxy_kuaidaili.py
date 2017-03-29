# -*- coding=utf-8 -*-
import requests
from lxml import html
import execjs
import re


def exception_decorator(func):  # 可以这样用，但是这样的变相异常处理，范围太大
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(u"sorry, 抓取出错。错误原因:", e)
    return decorate


class GetFreeProxy(object):
    def __init__(self, max_page=1):
        self.max_page = max_page
        self.proxies = []
        self.checked_proies = []
        self.session = requests.Session()
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        self.session.headers.update(self.headers)
        self.url_list = []

    def get_dom_tree(self, url):
        page = self.session.get(url=url, headers=self.headers, timeout=30)
        return html.fromstring(page.content)

    @exception_decorator
    def free_proxy_kuaidaili(self, page=10):  # 快代理

        # 之后的十多行只是为了拿到一个cookies
        dom = self.session.get('http://www.kuaidaili.com/proxylist/1/')
        open('tmp_kuaidaili.html', 'w').write(dom.text)
        file = open('tmp_kuaidaili.html', 'r').read()
        ret1 = re.findall(r'function (.*?)\(', file)[0]
        ret1 = re.findall(r'%s\((.*?)\)' % ret1, file)
        ret2 = 'var  ' + re.findall(r'var (.*?) </script>', \
                                    file, re.DOTALL)[0][:-25].replace(ret1[1], ret1[0]) + ' return po;'
        ret3 = execjs.exec_(ret2)
        k = ret3.split(';')[0].split("'")[1].split('=')[0]
        v = ret3.split(';')[0].split("'")[1].split('=')[1]
        # {'_ydclearance': '0ac1fa903ebbfd9ef7b1bd75-7e1f-4461-921c-c4b2afa95a10-1490785013'}
        self.session.cookies.update({k: v})

        # 开始翻页，拿到ip和port
        self.url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))
        for url in self.url_list:
            dom = self.get_dom_tree(url)
            proxy_list = dom.xpath('//div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                str_ip = proxy.xpath('.//td[@data-title="IP"]/text()')[0]
                str_port = proxy.xpath('.//td[@data-title="PORT"]/text()')[0]
                # 还有：匿名度、类型、get/post支持、位置、响应速度、最后验证时间
                self.proxies.append(str_ip + ':' + str_port)

        # 完成ip地址de规范和有效性验证
        verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        for tmp in self.proxies:
            if re.findall(verify_regex, tmp):

                proxies = {
                    'http': 'http://' + tmp,
                    'https': 'http://' + tmp
                }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)'
                }
                try:
                    r = requests.get('http://www.qq.com', proxies=proxies, headers=headers)
                    # self.checked_proies.append(tmp)
                except Exception as e:
                    print('代理有问题:', tmp, e)




if __name__ == '__main__':
    gg = GetFreeProxy()
    gg.free_proxy_kuaidaili()
    print('中找到:', len(gg.proxies))
    print('格式检查和可用检查', len(gg.checked_proies))
