# encoding: utf-8

"""
配置文件，一般来说不需要修改
如果需要启用或者经用某些网站的爬取器，可在网页上进行修改
"""

import os

# 数据库文件路径
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

# 每次运行所有爬取器之后，睡眠多少时间，单位秒
PROC_FETCHER_SLEEP = 5 * 60

# 验证器每次睡眠的时间，单位秒
PROC_VALIDATOR_SLEEP = 5

# 验证器的配置参数
VALIDATE_THREAD_NUM = 40 # 每批并行验证的代理数量
VALIDATE_URL = 'http://www.baidu.com'
VALIDATE_TIMEOUT = 8 # 超时时间，单位s
VALIDATE_MAX_FAILS = 3 # 3次尝试中只要有1次成功，就认为代理可用
