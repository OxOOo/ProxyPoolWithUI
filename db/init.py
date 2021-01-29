# encoding: utf-8

from config import DATABASE_PATH
from .Proxy import Proxy
from .Fetcher import Fetcher
from fetchers import fetchers
import sqlite3

def init():
    """
    初始化数据库
    """

    conn = sqlite3.connect(DATABASE_PATH)

    create_tables = [Proxy.ddl, Fetcher.ddl]
    for sql in create_tables:
        conn.execute(sql)
        conn.commit()
    
    # 注册所有的爬取器
    c = conn.cursor()
    c.execute('BEGIN EXCLUSIVE TRANSACTION;')
    for item in fetchers:
        c.execute('SELECT * FROM fetchers WHERE name=?', (item.name,))
        if c.fetchone() is None:
            f = Fetcher()
            f.name = item.name
            c.execute('INSERT INTO fetchers VALUES(?,?,?,?,?)', f.params())
    c.close()
    conn.commit()
    
    conn.close()
