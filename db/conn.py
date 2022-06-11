# encoding: utf-8

"""
封装的数据库接口
"""

from config import DATABASE_PATH
from .Proxy import Proxy
from .Fetcher import Fetcher
import sqlite3
import datetime
import threading

conn = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
# 线程锁
conn_lock = threading.Lock()
# 进程锁
proc_lock = None

def set_proc_lock(proc_lock_sub):
    """
    设置进程锁
    proc_lock_sub : main中的进程锁
    """
    global proc_lock
    proc_lock = proc_lock_sub

def pushNewFetch(fetcher_name, protocol, ip, port):
    """
    爬取器新抓到了一个代理，调用本函数将代理放入数据库
    fetcher_name : 爬取器名称
    protocol : 代理协议
    ip : 代理IP地址
    port : 代理端口
    """
    p = Proxy()
    p.fetcher_name = fetcher_name
    p.protocol = protocol
    p.ip = ip
    p.port = port
    conn_lock.acquire()
    proc_lock.acquire()

    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    # 更新proxies表
    c.execute('SELECT * FROM proxies WHERE protocol=? AND ip=? AND port=?', (p.protocol, p.ip, p.port))
    row = c.fetchone()
    if row is not None: # 已经存在(protocol, ip, port)
        old_p = Proxy.decode(row)
        c.execute("""
            UPDATE proxies SET fetcher_name=?,to_validate_date=? WHERE protocol=? AND ip=? AND port=?
        """, (p.fetcher_name, min(datetime.datetime.now(), old_p.to_validate_date), p.protocol, p.ip, p.port))
    else:
        c.execute('INSERT INTO proxies VALUES (?,?,?,?,?,?,?,?,?)', p.params())
    c.close()
    conn.commit()
    conn_lock.release()
    proc_lock.release()

def getToValidate(max_count=1):
    """
    从数据库中获取待验证的代理，根据to_validate_date字段
    优先选取已经通过了验证的代理，其次是没有通过验证的代理
    max_count : 返回数量限制
    返回 : list[Proxy]
    """
    conn_lock.acquire()
    proc_lock.acquire()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('SELECT * FROM proxies WHERE to_validate_date<=? AND validated=? ORDER BY to_validate_date LIMIT ?', (
        datetime.datetime.now(),
        True,
        max_count
    ))
    proxies = [Proxy.decode(row) for row in c]
    c.execute('SELECT * FROM proxies WHERE to_validate_date<=? AND validated=? ORDER BY to_validate_date LIMIT ?', (
        datetime.datetime.now(),
        False,
        max_count - len(proxies)
    ))
    proxies = proxies + [Proxy.decode(row) for row in c]
    c.close()
    conn.commit()
    conn_lock.release()
    proc_lock.release()
    return proxies

def pushValidateResult(proxy, success, latency):
    """
    将验证器的一个结果添加进数据库中
    proxy : 代理
    success : True/False，验证是否成功
    latency : 本次验证所用的时间(单位毫秒)
    """
    p = proxy
    should_remove = p.validate(success, latency)
    conn_lock.acquire()
    proc_lock.acquire()
    if should_remove:
        conn.execute('DELETE FROM proxies WHERE protocol=? AND ip=? AND port=?', (p.protocol, p.ip, p.port))
    else:
        conn.execute("""
            UPDATE proxies
            SET fetcher_name=?,validated=?,latency=?,validate_date=?,to_validate_date=?,validate_failed_cnt=?
            WHERE protocol=? AND ip=? AND port=?
        """, (
            p.fetcher_name, p.validated, p.latency, p.validate_date, p.to_validate_date, p.validate_failed_cnt,
            p.protocol, p.ip, p.port
        ))
    conn.commit()
    conn_lock.release()
    proc_lock.release()

def getValidatedRandom(max_count):
    """
    从通过了验证的代理中，随机选择max_count个代理返回
    max_count<=0表示不做数量限制
    返回 : list[Proxy]
    """
    conn_lock.acquire()
    proc_lock.acquire()
    if max_count > 0:
        r = conn.execute('SELECT * FROM proxies WHERE validated=? ORDER BY RANDOM() LIMIT ?', (True, max_count))
    else:
        r = conn.execute('SELECT * FROM proxies WHERE validated=? ORDER BY RANDOM()', (True,))
    proxies = [Proxy.decode(row) for row in r]
    r.close()
    conn_lock.release()
    proc_lock.release()
    return proxies

def pushFetcherResult(name, proxies_cnt):
    """
    更新爬取器的状态，每次在完成一个网站的爬取之后，调用本函数
    name : 爬取器的名称
    proxies_cnt : 本次爬取到的代理数量
    """
    conn_lock.acquire()
    proc_lock.acquire()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('SELECT * FROM fetchers WHERE name=?', (name,))
    row = c.fetchone()
    if row is None:
        raise ValueError(f'ERRROR: can not find fetcher {name}')
    else:
        f = Fetcher.decode(row)
        f.last_proxies_cnt = proxies_cnt
        f.sum_proxies_cnt = f.sum_proxies_cnt + proxies_cnt
        f.last_fetch_date = datetime.datetime.now()
        c.execute('UPDATE fetchers SET sum_proxies_cnt=?,last_proxies_cnt=?,last_fetch_date=? WHERE name=?', (
            f.sum_proxies_cnt, f.last_proxies_cnt, f.last_fetch_date, f.name
        ))
    c.close()
    conn.commit()
    conn_lock.release()
    proc_lock.release()

def pushFetcherEnable(name, enable):
    """
    设置是否起用对应爬取器，被禁用的爬取器将不会被运行
    name : 爬取器的名称
    enable : True/False, 是否启用
    """
    conn_lock.acquire()
    proc_lock.acquire()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('SELECT * FROM fetchers WHERE name=?', (name,))
    row = c.fetchone()
    if row is None:
        raise ValueError(f'ERRROR: can not find fetcher {name}')
    else:
        f = Fetcher.decode(row)
        f.enable = enable
        c.execute('UPDATE fetchers SET enable=? WHERE name=?', (
            f.enable, f.name
        ))
    c.close()
    conn.commit()
    conn_lock.release()
    proc_lock.release()

def getAllFetchers():
    """
    获取所有的爬取器以及状态
    返回 : list[Fetcher]
    """
    conn_lock.acquire()
    proc_lock.acquire()
    r = conn.execute('SELECT * FROM fetchers')
    fetchers = [Fetcher.decode(row) for row in r]
    r.close()
    conn_lock.release()
    proc_lock.release()
    return fetchers

def getFetcher(name):
    """
    获取指定爬取器以及状态
    返回 : Fetcher
    """
    conn_lock.acquire()
    proc_lock.acquire()
    r = conn.execute('SELECT * FROM fetchers WHERE name=?', (name,))
    row = r.fetchone()
    r.close()
    conn_lock.release()
    proc_lock.release()
    if row is None:
        return None
    else:
        return Fetcher.decode(row)

def getProxyCount(fetcher_name):
    """
    查询在数据库中有多少个由指定爬取器爬取到的代理
    fetcher_name : 爬取器名称
    返回 : int
    """
    conn_lock.acquire()
    proc_lock.acquire()
    r = conn.execute('SELECT count(*) FROM proxies WHERE fetcher_name=?', (fetcher_name,))
    cnt = r.fetchone()[0]
    r.close()
    conn_lock.release()
    proc_lock.release()
    return cnt

def getProxiesStatus():
    """
    获取代理状态，包括`全部代理数量`，`当前可用代理数量`，`等待验证代理数量`
    返回 : dict
    """
    conn_lock.acquire()
    proc_lock.acquire()
    r = conn.execute('SELECT count(*) FROM proxies')
    sum_proxies_cnt = r.fetchone()[0]
    r.close()

    r = conn.execute('SELECT count(*) FROM proxies WHERE validated=?', (True,))
    validated_proxies_cnt = r.fetchone()[0]
    r.close()

    r = conn.execute('SELECT count(*) FROM proxies WHERE to_validate_date<=?', (datetime.datetime.now(),))
    pending_proxies_cnt = r.fetchone()[0]
    r.close()
    conn_lock.release()
    proc_lock.release()
    return dict(
        sum_proxies_cnt=sum_proxies_cnt,
        validated_proxies_cnt=validated_proxies_cnt,
        pending_proxies_cnt=pending_proxies_cnt
    )

def pushClearFetchersStatus():
    """
    清空爬取器的统计信息，包括sum_proxies_cnt,last_proxies_cnt,last_fetch_date
    """
    conn_lock.acquire()
    proc_lock.acquire()
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    c.execute('UPDATE fetchers SET sum_proxies_cnt=?, last_proxies_cnt=?, last_fetch_date=?', (0, 0, None))
    c.close()
    conn.commit()
    conn_lock.release()
    proc_lock.release()
