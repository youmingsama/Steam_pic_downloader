import requests

# 获取连接请求
def get_data(link,port):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'timezoneOffset=28800,0;'

        }
        retry_count = 5
        while retry_count > 0:
            try:
                if port == '':
                    r = requests.get(link, headers=headers)
                else:
                    proxies = {'http': 'http://localhost:' + port, 'https': 'http://localhost:' + port}
                    r = requests.get(link, headers=headers, proxies=proxies)
                break
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        r.encoding = 'utf-8-sig'
        result = r.text

    except Exception as e:
        error_line = e.__traceback__.tb_lineno
        error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
        print(error_info)
        result = ''
    return result

def get_pic(link,port):
    try:
        retry_count = 5
        while retry_count > 0:
            try:
                if port == '':
                    r = requests.get(link)
                else:
                    proxies = {'http': 'http://localhost:' + port, 'https': 'http://localhost:' + port}
                    r = requests.get(link, proxies=proxies)
                break
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        # delete_proxy(proxy)
        result = r

    except Exception as e:
        error_line = e.__traceback__.tb_lineno
        error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
        print(error_info)
        result = ''
    return result