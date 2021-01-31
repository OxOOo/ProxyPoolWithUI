# encoding: utf-8

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from multiprocessing import Process
import time
from proc import run_fetcher, run_validator
from api import api

def main():
    processes = []
    processes.append(Process(target=run_fetcher.main, name='fetcher'))
    processes.append(Process(target=run_validator.main, name='validator'))
    processes.append(Process(target=api.main, name='api'))

    for p in processes:
        p.start()
        print(f'启动{p.name}进程，pid={p.pid}')
    while True:
        has_error = False
        for p in processes:
            if p.exitcode is not None:
                print(f'进程{p.name}异常推出, exitcode={p.exitcode}')
                has_error = True
                break
        if has_error:
            break
        time.sleep(0.2)
    for p in processes:
        if p.exitcode is None:
            p.terminate()

if __name__ == '__main__':
    main()
