# encoding: utf-8

from collections import namedtuple
Fetcher = namedtuple('Fetcher', ['name', 'fetcher'])

from .KuaidailiFetcher import KuaidailiFetcher
from .GoubanjiaFetcher import GoubanjiaFetcher
from .IP66Fetcher import IP66Fetcher
from .IP3366Fetcher import IP3366Fetcher
from .JiangxianliFetcher import JiangxianliFetcher
from .IHuanFetcher import IHuanFetcher

fetchers = [
    Fetcher(name='www.kuaidaili.com', fetcher=KuaidailiFetcher),
    Fetcher(name='www.goubanjia.com', fetcher=GoubanjiaFetcher),
    Fetcher(name='www.66ip.cn', fetcher=IP66Fetcher),
    Fetcher(name='www.ip3366.net', fetcher=IP3366Fetcher),
    Fetcher(name='ip.jiangxianli.com', fetcher=JiangxianliFetcher),
    Fetcher(name='ip.ihuan.me', fetcher=IHuanFetcher),
]
