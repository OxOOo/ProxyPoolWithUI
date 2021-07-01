import re
import time

import requests
from pyquery import PyQuery as pq

from .BaseFetcher import BaseFetcher


class XiLaFetcher(BaseFetcher):
    """
    'http://www.xiladaili.com/gaoni/
    """
    index = 0

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocol是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        self.index += 1
        new_index = self.index % 30

        urls = []
        urls = urls + [f'http://www.xiladaili.com/gaoni/{page}/' for page in range(new_index, new_index + 11)]
        urls = urls + [f'http://www.xiladaili.com/http/{page}/' for page in range(new_index, new_index + 11)]

        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')

        for url in urls:
            time.sleep(1)
            html = requests.get(url, timeout=10).text
            doc = pq(html)
            for line in doc('tr').items():
                tds = list(line('td').items())
                if len(tds) >= 2:
                    ip = tds[0].text().strip().split(":")[0]
                    port = tds[0].text().strip().split(":")[1]
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append(('http', ip, int(port)))

        return list(set(proxies))
