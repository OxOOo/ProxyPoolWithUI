# encoding: utf-8
"""
定时运行验证器
"""

import sys
import socket
import threading
from queue import Queue
import logging
import time
import requests
from db import conn
from config import PROC_VALIDATOR_SLEEP, VALIDATE_THREAD_NUM, VALIDATE_URL, VALIDATE_TIMEOUT, VALIDATE_MAX_FAILS

logging.basicConfig(stream=sys.stdout, format="%(asctime)s-%(levelname)s:%(name)s:%(message)s", level='INFO')

def main():
    """
    定时运行验证器
    主要逻辑：
    While True:
        从数据库中获取当前待验证的代理，最多VALIDATE_THREAD_NUM个
        对每个代理启动一个线程进行验证
    """
    logger = logging.getLogger('validator')

    in_que = Queue()
    out_que = Queue()
    running_proxies = set() # 储存哪些代理正在运行，以字符串的形式储存

    threads = []
    for _ in range(VALIDATE_THREAD_NUM):
        threads.append(threading.Thread(target=validate_thread, args=(in_que, out_que)))
    [_.start() for _ in threads]

    while True:
        out_cnt = 0
        while not out_que.empty():
            proxy, success = out_que.get()
            conn.pushValidateResult(proxy, success)
            uri = f'{proxy.protocal}://{proxy.ip}:{proxy.port}'
            assert uri in running_proxies
            running_proxies.remove(uri)
            out_cnt = out_cnt + 1
        if out_cnt > 0:
            logger.info(f'完成了{out_cnt}个代理的验证')
        
        if len(running_proxies) >= VALIDATE_THREAD_NUM:
            time.sleep(PROC_VALIDATOR_SLEEP)
            continue

        # 找一些新的待验证的代理放入队列中
        for proxy in conn.getToValidate(VALIDATE_THREAD_NUM):
            uri = f'{proxy.protocal}://{proxy.ip}:{proxy.port}'
            # 这里找出的代理有可能是正在进行验证的代理，要避免重复加入
            if uri not in running_proxies:
                running_proxies.add(uri)
                in_que.put(proxy)

def validate_thread(in_que, out_que):
    """
    验证函数，这个函数会在一个线程中被调用
    in_que: 输入队列，用于接收验证任务
    out_que: 输出队列，用于返回验证结果
    in_que和out_que都是线程安全队列，并且如果队列为空，调用in_que.get()会阻塞线程
    """

    while True:
        proxy = in_que.get()

        success = False
        for _ in range(VALIDATE_MAX_FAILS):
            try:
                proxies = {
                    'http': f'{proxy.protocal}://{proxy.ip}:{proxy.port}',
                    'https': f'{proxy.protocal}://{proxy.ip}:{proxy.port}'
                }
                r = requests.get(VALIDATE_URL, timeout=VALIDATE_TIMEOUT, proxies=proxies)
                html = r.text
                if '百度一下，你就知道' in html:
                    success = True
                    break
            except Exception as e:
                pass

        out_que.put((proxy, success))
