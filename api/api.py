# encoding: utf-8

from flask import Flask
from flask import jsonify
from flask import request

try:
    from db import conn
except:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from db import conn

app = Flask(__name__)

# 可用于测试API状态
@app.route('/', methods=['GET'])
def ping():
    return 'API OK'

# 随机获取一个可用代理，如果没有可用代理则返回空白
@app.route('/fetch_random', methods=['GET'])
def fetch_random():
    proxies = conn.getValidatedRandom(1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocal}://{p.ip}:{p.port}'
    else:
        return ''

# 获取所有可用代理，如果没有可用代理则返回空白
@app.route('/fetch_all', methods=['GET'])
def fetch_all():
    proxies = conn.getValidatedRandom(-1)
    proxies = [f'{p.protocal}://{p.ip}:{p.port}' for p in proxies]
    return ','.join(proxies)

############# 以下API主要给网页使用 ################

# 获取代理状态
@app.route('/proxies_status', methods=['GET'])
def proxies_status():
    proxies = conn.getValidatedRandom(-1)
    proxies = sorted(proxies, key=lambda p: f'{p.protocal}://{p.ip}:{p.port}')
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


# 跨域支持
def after_request(resp):
    ALLOWED_ORIGIN = ['0.0.0.0', '127.0.0.1', 'localhost']
    if request.headers['origin']:
        for item in ALLOWED_ORIGIN:
            if item in request.headers['origin']:
                resp.headers['Access-Control-Allow-Origin'] = request.headers['origin']
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
app.after_request(after_request)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
