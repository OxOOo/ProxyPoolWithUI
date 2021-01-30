# 爬取器

所有的爬取器都在这个目录中，并且在`__init__.py`中进行了注册。

## 添加新的爬取器

本项目默认包含了数量不少的免费公开代理源，并且会持续更新，如果你发现有不错的免费代理源，欢迎通过Issues反馈给我们。

1. 编写爬取器代码

爬取器需要继承基类`BaseFetcher`，然后实现`fetch`函数。

`fetch`函数没有输入参数，每次运行都返回一个列表，包含本次爬取到的代理。返回的格式为(代理协议类型,代理IP,端口)。

示例：

```python
class CustomFetcher(BaseFetcher):
    def fetch(self):
        return [('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
```

2. 注册爬取器

编写好爬取器之后，还需要在`__init__.py`文件中进行注册，添加如下代码：

**注意：爬取器的名称(name)一定不能重复。**

```python
from .CustomFetcher import CustomFetcher

fetchers = [
    ...
    Fetcher(name='www.custom.com', fetcher=CustomFetcher),
    ...
]
```

3. 重启

完成上述步骤之后，重启进程即可。代码会自动将新爬取器添加到数据库中，爬取进程也会自动运行新爬取器。
