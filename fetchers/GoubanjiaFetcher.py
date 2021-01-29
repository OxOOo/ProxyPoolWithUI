# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re

class GoubanjiaFetcher(BaseFetcher):
    """
    http://www.goubanjia.com/
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocal, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """

        proxies = []

        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
        html = requests.get('http://www.goubanjia.com/', headers=headers, timeout=10).text
        doc = pq(html)
        for item in doc('table tbody tr').items():
            ipport = item.find('td.ip').html()
            # 以下对ipport进行整理
            hide_reg = re.compile(r'<p[^<>]*style="display:[^<>]*none;"[^<>]*>[^<>]*</p>')
            ipport = re.sub(hide_reg, '', ipport)
            tag_reg = re.compile(r'<[^<>]*>')
            ipport = re.sub(tag_reg, '', ipport)

            ip = ipport.split(':')[0]
            port = self.pde(item.find('td.ip').find('span.port').attr('class').split(' ')[1])
            proxies.append(('http', ip, int(port)))
        
        return list(set(proxies))
    
    def pde(self, class_key): # 解密函数，端口是加密过的
        """
        key是class内容
        """
        class_key = str(class_key)
        f = []
        for i in range(len(class_key)):
            f.append(str('ABCDEFGHIZ'.index(class_key[i])))
        return str(int(''.join(f)) >> 0x3)
