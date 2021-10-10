# encoding: utf-8

from collections import namedtuple

Fetcher = namedtuple('Fetcher', ['name', 'fetcher'])

from .UUFetcher import UUFetcher
from .KuaidailiFetcher import KuaidailiFetcher
from .GoubanjiaFetcher import GoubanjiaFetcher
from .IP66Fetcher import IP66Fetcher
from .IP3366Fetcher import IP3366Fetcher
from .JiangxianliFetcher import JiangxianliFetcher
from .IHuanFetcher import IHuanFetcher
from .IP89Fetcher import IP89Fetcher
from .ProxyscanFetcher import ProxyscanFetcher
from .KaiXinFetcher import KaiXinFetcher
from .XiLaFetcher import XiLaFetcher
from .XiaoShuFetcher import XiaoShuFetcher
from .ProxyListFetcher import ProxyListFetcher
from .ProxyScrapeFetcher import ProxyScrapeFetcher

fetchers = [
    Fetcher(name='uu-proxy.com', fetcher=UUFetcher),
    Fetcher(name='www.kuaidaili.com', fetcher=KuaidailiFetcher),
    Fetcher(name='www.goubanjia.com', fetcher=GoubanjiaFetcher),
    Fetcher(name='www.66ip.cn', fetcher=IP66Fetcher),
    Fetcher(name='www.ip3366.net', fetcher=IP3366Fetcher),
    Fetcher(name='ip.jiangxianli.com', fetcher=JiangxianliFetcher),
    Fetcher(name='ip.ihuan.me', fetcher=IHuanFetcher),
    Fetcher(name='www.proxyscan.io', fetcher=ProxyscanFetcher),
    Fetcher(name='www.89ip.cn', fetcher=IP89Fetcher),
    Fetcher(name='www.kxdaili.com', fetcher=KaiXinFetcher),
    Fetcher(name='www.xiladaili.com', fetcher=XiLaFetcher),
    Fetcher(name='www.xsdaili.cn', fetcher=XiaoShuFetcher),
    Fetcher(name='www.proxy-list.download', fetcher=ProxyListFetcher),
    Fetcher(name='proxyscrape.com', fetcher=ProxyScrapeFetcher)
]
