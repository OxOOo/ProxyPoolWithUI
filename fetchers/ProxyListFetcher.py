import time

import requests

from .BaseFetcher import BaseFetcher


class ProxyListFetcher(BaseFetcher):
    """
    https://www.proxy-list.download/api/v1/get?type={{ protocol }}&_t={{ timestamp }}
    """

    def fetch(self):
        proxies = []
        type_list = ['socks4', 'socks5', 'http', 'https']
        for protocol in type_list:
            url = "https://www.proxy-list.download/api/v1/get?type=" + protocol + "&_t=" + str(time.time())
            proxies_list = requests.get(url).text.split("\n")
            for data in proxies_list:
                flag_idx = data.find(":")
                ip = data[:flag_idx]
                port = data[flag_idx + 1:-1]
                proxies.append((protocol, ip, port))

        return list(set(proxies))
