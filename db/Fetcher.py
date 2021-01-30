# encoding: utf-8

import datetime

class Fetcher(object):
    """
    爬取器的状态储存在数据库中，包括是否启用爬取器，爬取到的代理数量等
    """

    ddl = """
    CREATE TABLE IF NOT EXISTS fetchers
    (
        name VARCHAR(255) NOT NULL,
        enable BOOLEAN NOT NULL,
        sum_proxies_cnt INTEGER NOT NULL,
        last_proxies_cnt INTEGER NOT NULL,
        last_fetch_date TIMESTAMP,
        PRIMARY KEY (name)
    )
    """

    def __init__(self):
        self.name = None
        self.enable = True
        self.sum_proxies_cnt = 0
        self.last_proxies_cnt = 0
        self.last_fetch_date = None
    
    def params(self):
        """
        返回一个元组，包含自身的全部属性
        """
        return (
            self.name, self.enable,
            self.sum_proxies_cnt, self.last_proxies_cnt, self.last_fetch_date
        )
    
    def to_dict(self):
        """
        返回一个dict，包含自身的全部属性
        """
        return {
            'name': self.name,
            'enable': self.enable,
            'sum_proxies_cnt': self.sum_proxies_cnt,
            'last_proxies_cnt': self.last_proxies_cnt,
            'last_fetch_date': self.last_fetch_date
        }
    
    @staticmethod
    def decode(row):
        """
        将sqlite返回的一行解析为Fetcher
        row : sqlite返回的一行
        """
        assert len(row) == 5
        f = Fetcher()
        f.name = row[0]
        f.enable = bool(row[1])
        f.sum_proxies_cnt = row[2]
        f.last_proxies_cnt = row[3]
        f.last_fetch_date = row[4]
        return f
