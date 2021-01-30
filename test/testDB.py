# encoding: utf-8

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from db import conn

def run():
    assert len(conn.getToValidate(10)) == 0
    conn.pushNewFetch('test', 'http', '127.0.0.1', 8080)
    assert len(conn.getToValidate(10)) == 1

    conn.pushNewFetch('test', 'http', '127.0.0.2', 8080)
    conn.pushNewFetch('test', 'http', '127.0.0.3', 8080)
    conn.pushNewFetch('test', 'http', '127.0.0.4', 8080)
    assert len(conn.getToValidate(2)) == 2
    proxies = conn.getToValidate(10)
    assert len(proxies) == 4
    assert proxies[0].ip == '127.0.0.1'
    assert proxies[1].ip == '127.0.0.2'
    assert proxies[2].ip == '127.0.0.3'
    assert proxies[3].ip == '127.0.0.4'

    p = conn.getToValidate(1)[0] # 设置一个通过验证
    conn.pushValidateResult(p, True)
    assert len(conn.getToValidate(10)) == 3
    p = conn.getToValidate(1)[0] # 设置一个没有通过验证
    conn.pushValidateResult(p, False)
    assert len(conn.getToValidate(10)) == 2
    assert len(conn.getValidatedRandom(1)) == 1
    assert len(conn.getValidatedRandom(-1)) == 1
    p = conn.getValidatedRandom(1)[0]
    assert p.ip == '127.0.0.1'
    p = conn.getToValidate(1)[0] # 设置一个通过验证
    conn.pushValidateResult(p, True)
    assert len(conn.getValidatedRandom(1)) == 1
    assert len(conn.getValidatedRandom(-1)) == 2

    fetchers = conn.getAllFetchers()
    for item in fetchers:
        # 所有爬取器都应该是默认参数
        assert item.enable == True
        assert item.sum_proxies_cnt == 0
        assert item.last_proxies_cnt == 0
        assert item.last_fetch_date is None
    conn.pushFetcherResult('www.kuaidaili.com', 10)
    conn.pushFetcherResult('www.kuaidaili.com', 20)
    conn.pushFetcherEnable('www.kuaidaili.com', False)
    f = conn.getFetcher('www.kuaidaili.com')
    assert f is not None
    # www.kuaidaili.com的参数应该被修改了
    assert f.enable == False
    assert f.sum_proxies_cnt == 30
    assert f.last_proxies_cnt == 20
    assert f.last_fetch_date is not None

if __name__ == '__main__':
    print(u'请确保运行本脚本之前删除或备份`data.db`文件')
    run()
    print(u'测试通过')
