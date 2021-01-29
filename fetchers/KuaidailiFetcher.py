# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq

class KuaidailiFetcher(BaseFetcher):
    """
    https://www.kuaidaili.com/free
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocal, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        
        urls = []
        urls = urls + [f'https://www.kuaidaili.com/free/inha/{page}/' for page in range(1, 11)]
        urls = urls + [f'https://www.kuaidaili.com/free/intr/{page}/' for page in range(1, 11)]

        proxies = []

        for url in urls:
            html = requests.get(url, timeout=10).text
            doc = pq(html)
            for item in doc('table tbody tr').items():
                ip = item.find('td[data-title="IP"]').text()
                port = int(item.find('td[data-title="PORT"]').text())
                proxies.append(('http', ip, port))
        
        return list(set(proxies))
