from unittest import result
import requests
import hashlib
from bot_func.constant import appid, key, salt


def auto2en(q: str) -> str:
    """
    翻译为英文。
    """
    sign = hashlib.md5((appid + q + salt + key).encode('utf-8')).hexdigest()
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate?q=%s&from=auto&to=en&appid=%s&salt=%s&sign=%s' % (q, appid, salt, sign)
    response = requests.get(url)
    if response.status_code == 200:
        trans_json = response.json()
        if 'trans_result' in trans_json:
            trans_result = trans_json['trans_result'][0]
            return trans_result['dst']
        else:
            return '说太快了啦！反应不过来了呜...'
    else:
        return '二澪听不懂呢(*>﹏<*)'


if __name__ == '__main__':
    print(auto2en('我是傻逼'))
