import re

import requests

from .BaseFetcher import BaseFetcher


class ProxyScanFetcher(BaseFetcher):
    """
    https://www.proxyscan.io
    """
    index = 0

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocol是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """

        url = "https://www.proxyscan.io/download?type=http"

        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')

        html = requests.get(url, timeout=10).text
        for item in html.split("\n"):
            try:
                ip = item.split(":")[0]
                port = item.split(":")[1]
                proxies.append(('http', ip, int(port)))
                if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                    proxies.append(('http', ip, int(port)))
            except Exception:
                continue

        return list(set(proxies))
