# 简易好用的代理池

* 定时自动爬取网络上的免费代理
* 定时对代理进行验证，集成API随时返回可用代理
* 不需要第三方数据库支持，一键启动，简单易用
* 集成WEB管理界面，方便查看代理状态并对代理池进行配置

如果你知道有好用的代理源，或者是发现本项目存在一些问题，欢迎通过Issues和我们讨论。

## WEB管理界面截图

![screenshot1](docs/screenshot1.png)
![screenshot2](docs/screenshot2.png)

## 已经集成的免费代理源

| 名称         | 地址                        |
|--------------|-----------------------------|
| 快代理       | https://www.kuaidaili.com/  |
| 全网代理     | http://www.goubanjia.com/   |
| 66代理       | http://www.66ip.cn/         |
| 云代理       | http://www.ip3366.net/      |
| 免费代理库   | https://ip.jiangxianli.com/ |
| 小幻HTTP代理 | https://ip.ihuan.me/        |
| 89免费代理   | https://www.89ip.cn/        |

## 运行本项目

本项目目前只适配了Python3,请确保你的电脑上安装了3.6或更高版本的Python软件。

1. 下载代码

```bash
git clone https://github.com/believedotchenyu/ProxyPoolWithUI.git
```

2. 安装Python依赖(在`ProxyPoolWithUI`目录下执行)

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

3. 启动(在`ProxyPoolWithUI`目录下执行)

```bash
python3 main.py
```

如果你在运行了上述命令之后，在命令行中看到了类似如下截图，那么说明项目成功启动了：

![term](docs/term.png)

4. 使用浏览器打开`http://localhost:5000`，可以看到WEB管理界面。

## 使用代理

1. API接口

项目启动之后，会自动爬取并检测代理是否可用，因此我们只需要关注如何使用代理即可。

* `http://localhost:5000/fetch_random` : 随机获取一个可用代理，如果没有可用代理则返回空白
  
  返回示例 : `http://127.0.0.1:8080`

* `http://localhost:5000/fetch_all` : 获取所有可用代理，如果没有可用代理则返回空白
  
  返回示例 : `http://127.0.0.1:8080,http://127.0.0.1:8081`

1. 使用代理

不同语言使用代理的方式各不相同，这里提供一个Python集成本项目并使用代理的示例代码：

```python
# encoding : utf-8

import requests

def main():
    proxy_uri = requests.get('http://localhost:5000/fetch_random').text
    if len(proxy_uri) == 0:
        print(u'暂时没有可用代理')
        return
    
    proxies = { 'http': proxy_uri }
    html = requests.get('http://www.baidu.com', proxies=proxies)
    if u'百度一下，你就知道' in html:
        print('代理可用')
    else:
        print('代理不可用')

if __name__ == '__main__':
    main()
```

## 配置

如果是需要禁用或者启用某些代理，可直接在WEB管理界面进行操作。

本项目的大部分配置均可在`config.py`中找到，默认配置已经可以适应绝大部分情况，一般来说不需要进行修改。

## 添加新的代理源

本项目的爬取器均在`fetchers`目录下，你也可以根据自己的需求对其中的爬取器进行修改或者扩展。

对本项目扩展爬取器并不复杂，详细的操作步骤可见[此处](fetchers/)，可以参考`fetchers`目录下已有的爬取器。
