from bot_func.send import send_group
from random import randint
from bot_func.constant import group_id


def errand(list_input: list) -> None:
    max = len(list_input) - 1
    if max >= 0:
        sel = randint(0, max)
        send_group(list_input[sel], group_id)
    else:
        send_group('什么参数都没有，说点什么吧', group_id)


if __name__ == '__main__':
    print(randint(0, 0))
