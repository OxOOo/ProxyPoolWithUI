# encoding : utf-8

import requests

def main():
    proxy_uri = 'http://223.10.82.66:8118'
    # proxy_uri = 'http://localhost:8118'
    if len(proxy_uri) == 0:
        print(u'暂时没有可用代理')
        return
    print(u'获取到的代理是：' + proxy_uri)
    
    proxies = { 'http': proxy_uri, 'https': proxy_uri }
    # headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    html = requests.get('https://www.baidu.com', proxies=proxies).text
    print(html)

if __name__ == '__main__':
    main()