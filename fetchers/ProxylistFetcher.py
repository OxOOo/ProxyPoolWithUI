from .BaseFetcher import BaseFetcher
import requests
import time

class ProxylistFetcher(BaseFetcher):
    """
    https://www.proxy-list.download/api/v1/get?type={{ protocol }}&_t={{ timestamp }}
    """

    def fetch(self):
        proxies = []
        type_list = ['socks4', 'socks5', 'http', 'https']
        for protocol in type_list:
            url = "http://1.0.0.3/api/v1/get?type=" + protocol + "&_t=" + str(time.time())
            headers = {
                "HOST": "www.proxy-list.download"
            }
            resp = requests.get(url, headers=headers).text
            for data in resp.split("\n"):
                flag_idx = data.find(":")
                ip = data[:flag_idx]
                port = data[flag_idx + 1:-1]
                proxies.append((protocol, ip, port))

        return list(set(proxies))
