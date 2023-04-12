import requests


def set_friend(flag):
    """
    通过好友请求。
    """
    print(flag)
    requests.get('http://127.0.0.1:5700/set_friend_add_request?flag=%s' % flag)


if __name__ == '__main__':
    print('ssss%b' % True)
