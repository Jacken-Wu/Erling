from bot_func.constant import group_id
from bot_func.send import send_group
import random


def respond_group(words: str) -> None:
    """
    满足以下条件时二澪应和用户的发言。
    """
    if words in ['你说是吧二澪', '你说对吧二澪', '对吧二澪']:
        sel = random.randint(0, 2)
        back = 'sodayo'
        if sel == 0:
            back = 'sodayo'
        elif sel == 1:
            back = 'sodayo~'
        elif sel == 2:
            back = '嗯'
        send_group(back, group_id)

    elif words[-1] == ' ':
        sel = random.randint(0, 2)
        back = '好好好'
        if sel == 0:
            back = '好好好'
        elif sel == 1:
            back = '太对了'
        elif sel == 2:
            back = '就是就是'
        send_group(back, group_id)