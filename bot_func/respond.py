from bot_func.constant import group_id
from bot_func.send import send_group
from bot_func.erlove import get_respond
import random


def respond_group(user_id: int, words: str) -> None:
    """
    满足以下条件时二澪应和用户的发言。
    """
    if (len(words) > 3) and (words[-3:] in ['，二澪', ',二澪']):
        sel = random.randint(0, 7)
        back = 'sodayo'
        if sel == 0:
            back = 'sodayo'
        elif sel == 1:
            back = 'sodayo~'
        elif sel == 2:
            back = '嗯'
        elif sel == 3:
            back = '对呀'
        elif sel == 4:
            back = '对呀对呀'
        elif sel == 5:
            back = '就是'
        elif sel == 6:
            back = '就是就是'
        elif sel == 7:
            back = '没错'
        send_group(back, group_id)

    elif words[-1] == ' ':
        back = get_respond(user_id)
        send_group(back, group_id)