# encoding: utf-8

import sys, os, signal
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from multiprocessing import Process
import time
from proc import run_fetcher, run_validator
from api import api
import multiprocessing

# 进程锁
proc_lock = multiprocessing.Lock()

class Item:
    def __init__(self, target, name):
        self.target = target
        self.name = name
        self.process = None
        self.start_time = 0

def main():
    processes = []
    processes.append(Item(target=run_fetcher.main, name='fetcher'))
    processes.append(Item(target=run_validator.main, name='validator'))
    processes.append(Item(target=api.main, name='api'))

    while True:
        for p in processes:
            if p.process is None:
                p.process = Process(target=p.target, name=p.name, daemon=False, args=(proc_lock, ))
                p.process.start()
                print(f'启动{p.name}进程，pid={p.process.pid}')
                p.start_time = time.time()

        for p in processes:
            if p.process is not None:
                if not p.process.is_alive():
                    print(f'进程{p.name}异常退出, exitcode={p.process.exitcode}')
                    p.process.terminate()
                    p.process = None
                elif p.start_time + 60 * 60 < time.time(): # 最长运行1小时就重启
                    print(f'进程{p.name}运行太久，重启')
                    p.process.terminate()
                    p.process = None

        time.sleep(0.2)

def citest():
    """
    此函数仅用于检查程序是否可运行，一般情况下使用本项目可忽略
    """
    processes = []
    processes.append(Item(target=run_fetcher.main, name='fetcher'))
    processes.append(Item(target=run_validator.main, name='validator'))
    processes.append(Item(target=api.main, name='api'))

    for p in processes:
        assert p.process is None
        p.process = Process(target=p.target, name=p.name, daemon=False)
        p.process.start()
        print(f'running {p.name}, pid={p.process.pid}')
        p.start_time = time.time()

    time.sleep(10)

    for p in processes:
        assert p.process is not None
        assert p.process.is_alive()
        p.process.terminate()

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == 'citest':
            citest()
        else:
            main()
        sys.exit(0)
    except Exception as e:
        print('========FATAL ERROR=========')
        print(e)
        sys.exit(1)
