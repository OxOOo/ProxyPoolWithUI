# encoding: utf-8

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from fetchers import fetchers

def run():
    proxies_cnt = dict()
    for item in fetchers:
        if item.name != 'uu-proxy.com': continue # 这行表示只测试特定的爬取器

        print('='*10, 'RUNNING ' + item.name, '='*10)
        fetcher = item.fetcher() # 实例化爬取器
        try:
            proxies = fetcher.fetch()
        except Exception as e:
            print(e)
            proxies = []
        print(proxies)
        proxies_cnt[item.name] = len(proxies)
    
    print('='*10, 'PROXIES CNT', '='*10)
    print(proxies_cnt)

if __name__ == '__main__':
    run()
