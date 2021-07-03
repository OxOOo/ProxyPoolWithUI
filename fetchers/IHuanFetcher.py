# encoding: utf-8
import time

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re


class IHuanFetcher(BaseFetcher):
    """
    https://ip.ihuan.me/
    爬这个网站要温柔点，站长表示可能会永久关站
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """

        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')
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


        def getSingePage(url):
            try:
                time.sleep(2)
                html = requests.get(url, headers=headers, timeout=10).text
                doc = pq(html)
            except Exception as e:
                print('ERROR in ip.ihuan.me:', e)
                return

            for line in doc('tbody tr').items():
                tds = list(line('td').items())
                if len(tds) == 10:
                    ip = tds[0].text().strip()
                    port = tds[1].text().strip()
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append(('http', ip, int(port)))


        def getPages(url_start):
            pending_urls = []
            url = url_start
            doc = pq("1234")

            try:
                html = requests.get(url, headers=headers, timeout=8).text
                doc = pq(html)
            except Exception as e:
                print('ERROR in ip.ihuan.me:', e)

            pending_urls.append(url_start)
            for item in list(doc('.pagination a').items())[1:-1]:
                href = item.attr('href')
                if href is not None and href.startswith('?page='):
                    pending_urls.append('https://ip.ihuan.me/' + href)
            for url in pending_urls:
                getSingePage(url)
            return pending_urls[len(pending_urls) - 1]


        next_round = getPages("https://ip.ihuan.me/")
        for i in range(1, 4):
            next_round = getPages(next_round)
        return list(set(proxies))
