# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
import json

class UUFetcher(BaseFetcher):
    """
    https://uu-proxy.com/
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocal, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.130 Chrome/79.0.3945.130 Safari/537.36'
        }
        data = requests.get('https://uu-proxy.com/api/free', headers=headers, timeout=10).text
        free = json.loads(data)['free']
        proxies = [(item['scheme'], item['ip'], item['port']) for item in free['proxies']]

        return list(set(proxies))
