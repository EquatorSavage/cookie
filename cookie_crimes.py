import json
import requests
import websocket
"""
# 关闭edge： 必须没有msedge进程在启动着，否则下面命令虽然会启动edge进程，但是并不会开启远程调试端口。
Get-Process msedge | Stop-Process
以管理员身份运行cmd
# 启动远程调试:使用无头参数-headless存在的一个缺点，只能获取到打开的网站的Cookie。因此如果想要获取指定目标网站的Cookie，要么重复上面的动作，要么取消无头参数-headless
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" https://www.baidu.com --remote-debugging-port=9222  --remote-allow-origins=* -headless
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" https://www.baidu.com --remote-debugging-port=9222  --remote-allow-origins=*
"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.baidu.com --remote-debugging-port=9222  --remote-allow-origins=* -headless
"C:\Program Files\Google\Chrome\Application\chrome.exe" https://www.baidu.com --remote-debugging-port=9222  --remote-allow-origins=*
# 把远程调试端口映射出来
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=48333 connectaddress=127.0.0.1 connectport=9222
# 访问json接口获取websocket地址并获取Cookie
# 关闭端口映射
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=48333
"""

def hit_that_secret_json_path_like_its_1997():
    response = requests.get("http://127.0.0.1:48333/json")
    websocket_url = response.json()[0].get("webSocketDebuggerUrl")
    return websocket_url


def gimme_those_cookies(ws_url):
    ws = websocket.create_connection(ws_url)
    ws.send(json.dumps({"id": 1, "method": "Storage.getCookies"}))
    result = ws.recv()
    ws.close()
    response = json.loads(result)
    cookies = response["result"]["cookies"]
    return cookies

ws_url = hit_that_secret_json_path_like_its_1997()
print(ws_url)
cookies = gimme_those_cookies(ws_url)
# print(cookies)

def to_cookie_dict(data):
    if 'booktoki468.com' in data['domain']:
        cookie_dict = {data['name']: data['value'], 'Domain': data['domain'], 'Path': data['path'], 'Expires': data['expires']}
        print(cookie_dict)
        return cookie_dict

# data_list = [{}]
data_list = cookies

cookie_dict_list = [to_cookie_dict(data) for data in data_list]
cookie_dict_list = [c for c in cookie_dict_list if c is not None]

# 遍历多个cookie字典，将每个字典中的key和value格式化为key=value的字符串
cookie_str_list = []
for cookie_dict in cookie_dict_list:
    try:
        for k, v in cookie_dict.items():
            cookie_str_list.append('{}={}'.format(k, v))
    except Exception as e:
        print(e)
        pass

# 使用;将多个key=value字符串连接在一起
cookie_str = ';'.join(cookie_str_list)
print(cookie_str)