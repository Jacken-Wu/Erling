import requests
import random
import time
from bot_func.constant import father_id


def send_private(words: str, user_id: int) -> None:
    """
    私聊发送消息。
    """
    time.sleep(0.5 + random.random() * 1.5)
    requests.get('http://127.0.0.1:5700/send_private_msg?user_id=%d&message=%s' % (user_id, words))


def send_group(words: str, group_id: int) -> None:
    """
    群聊发送消息。
    """
    time.sleep(0.5 + random.random() * 1.5)
    requests.get('http://127.0.0.1:5700/send_group_msg?group_id=%d&message=%s' % (group_id, words))


def send_message(words: str) -> None:
    """
    向管理者发送私聊消息。
    """
    send_private(words, father_id)
