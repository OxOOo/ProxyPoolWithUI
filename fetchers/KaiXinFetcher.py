import re
import time

import requests
from pyquery import PyQuery as pq

from .BaseFetcher import BaseFetcher


class KaiXinFetcher(BaseFetcher):
    """
    http://www.kxdaili.com/dailiip
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocol是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """

        urls = []

        urls = urls + [f'http://www.kxdaili.com/dailiip/1/{page}.html' for page in range(1, 11)]

        urls = urls + [f'http://www.kxdaili.com/dailiip/2/{page}.html' for page in range(1, 11)]

        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')

        for url in urls:
            html = requests.get(url, timeout=10).text
            doc = pq(html)
            for line in doc('tr').items():
                tds = list(line('td').items())
                if len(tds) >= 2:
                    ip = tds[0].text().strip()
                    port = tds[1].text().strip()
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append(('http', ip, int(port)))

        return list(set(proxies))
