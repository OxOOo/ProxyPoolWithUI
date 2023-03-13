# encoding: utf-8

import os
import logging
from flask import Flask
from flask import jsonify, request, redirect, send_from_directory

log = logging.getLogger('werkzeug')
log.disabled = True

try:
    from db import conn
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from db import conn

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'frontend', 'deployment')

app = Flask(
    __name__,
    static_url_path='/web',
    static_folder=STATIC_FOLDER
)

############# 以下API可用于获取代理 ################

# 可用于测试API状态
@app.route('/ping', methods=['GET'])
def ping():
    return 'API OK'

# 随机获取一个可用代理，如果没有可用代理则返回空白
@app.route('/fetch_random', methods=['GET'])
def fetch_random():
    proxies = conn.getValidatedRandom(1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

############# 新增加接口int ################        

#api 获取协议为http的一条结果
@app.route('/fetch_http', methods=['GET'])
def fetch_http():
    proxies =conn.get_by_protocol('http', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为http的全部结果
@app.route('/fetch_http_all', methods=['GET'])
def fetch_http_all():
    proxies = conn.get_by_protocol('http', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
        
#api 获取协议为https的一条结果
@app.route('/fetch_https', methods=['GET'])
def fetch_https():
    proxies =conn.get_by_protocol('https', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为https的全部结果
@app.route('/fetch_https_all', methods=['GET'])
def fetch_https_all():
    proxies = conn.get_by_protocol('https', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
                
#api 获取协议为http的一条结果
@app.route('/fetch_socks4', methods=['GET'])
def fetch_socks4():
    proxies =conn.get_by_protocol('socks4', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为http的全部结果
@app.route('/fetch_socks4_all', methods=['GET'])
def fetch_socks4_all():
    proxies = conn.get_by_protocol('socks4', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
        
#api 获取协议为https的一条结果
@app.route('/fetch_socks5', methods=['GET'])
def fetch_socks5():
    proxies =conn.get_by_protocol('socks5', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为https的全部结果
@app.route('/fetch_socks5_all', methods=['GET'])
def fetch_socks5_all():
    proxies = conn.get_by_protocol('socks5', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
                        
############# 新增加接口end ################    

# 获取所有可用代理，如果没有可用代理则返回空白
@app.route('/fetch_all', methods=['GET'])
def fetch_all():
    proxies = conn.getValidatedRandom(-1)
    proxies = [f'{p.protocol}://{p.ip}:{p.port}' for p in proxies]
    return ','.join(proxies)

############# 以下API主要给网页使用 ################

@app.route('/')
def index():
    return redirect('/web')

# 网页：首页
@app.route('/web', methods=['GET'])
@app.route('/web/', methods=['GET'])
def page_index():
    return send_from_directory(STATIC_FOLDER, 'index.html')

# 网页：爬取器状态
@app.route('/web/fetchers', methods=['GET'])
@app.route('/web/fetchers/', methods=['GET'])
def page_fetchers():
    return send_from_directory(STATIC_FOLDER, 'fetchers/index.html')

# 获取代理状态
@app.route('/proxies_status', methods=['GET'])
def proxies_status():
    proxies = conn.getValidatedRandom(-1)
    proxies = sorted(proxies, key=lambda p: f'{p.protocol}://{p.ip}:{p.port}', reverse=True)
    proxies = [p.to_dict() for p in proxies]

    status = conn.getProxiesStatus()

    return jsonify(dict(
        success=True,
        proxies=proxies,
        **status
    ))

# 获取爬取器状态
@app.route('/fetchers_status', methods=['GET'])
def fetchers_status():
    proxies = conn.getValidatedRandom(-1) # 获取所有可用代理
    fetchers = conn.getAllFetchers()
    fetchers = [f.to_dict() for f in fetchers]

    for f in fetchers:
        f['validated_cnt'] = len([_ for _ in proxies if _.fetcher_name == f['name']])
        f['in_db_cnt'] = conn.getProxyCount(f['name'])
    
    return jsonify(dict(
        success=True,
        fetchers=fetchers
    ))

# 清空爬取器状态
@app.route('/clear_fetchers_status', methods=['GET'])
def clear_fetchers_status():
    conn.pushClearFetchersStatus()
    return jsonify(dict(success=True))

# 设置是否启用特定爬取器,?name=str,enable=0/1
@app.route('/fetcher_enable', methods=['GET'])
def fetcher_enable():
    name = request.args.get('name')
    enable = request.args.get('enable')
    if enable == '1':
        conn.pushFetcherEnable(name, True)
    else:
        conn.pushFetcherEnable(name, False)
    return jsonify(dict(success=True))

############# 其他 ################

# 跨域支持，主要是在开发网页端的时候需要使用
def after_request(resp):
    ALLOWED_ORIGIN = ['0.0.0.0', '127.0.0.1', 'localhost']
    origin = request.headers.get('origin', None)
    if origin is not None:
        for item in ALLOWED_ORIGIN:
            if item in origin:
                resp.headers['Access-Control-Allow-Origin'] = origin
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
app.after_request(after_request)

def main(proc_lock):
    if proc_lock is not None:
        conn.set_proc_lock(proc_lock)
    # 因为默认sqlite3中，同一个数据库连接不能在多线程环境下使用，所以这里需要禁用flask的多线程
    app.run(host='0.0.0.0', port=5000, threaded=False)

if __name__ == '__main__':
    main(None)
