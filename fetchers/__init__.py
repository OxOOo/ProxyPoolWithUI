# encoding: utf-8

from collections import namedtuple

Fetcher = namedtuple('Fetcher', ['name', 'fetcher'])

from .UUFetcher import UUFetcher
from .IP66Fetcher import IP66Fetcher
from .IP89Fetcher import IP89Fetcher
from .ProxyscanFetcher import ProxyscanFetcher
from .KaiXinFetcher import KaiXinFetcher
from .XiaoShuFetcher import XiaoShuFetcher



fetchers = [
    Fetcher(name='uu-proxy.com', fetcher=UUFetcher),
    Fetcher(name='www.66ip.cn', fetcher=IP66Fetcher),
    Fetcher(name='www.proxyscan.io', fetcher=ProxyscanFetcher),
    Fetcher(name='www.89ip.cn', fetcher=IP89Fetcher),
    Fetcher(name='www.kxdaili.com', fetcher=KaiXinFetcher),
    Fetcher(name='www.xsdaili.cn', fetcher=XiaoShuFetcher)
]
