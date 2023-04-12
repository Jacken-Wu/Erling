from bot_func.send import send_group
from bot_func.constant import group_id, data_path
import random


def words_cmp(words: str) -> bool:
    """
    判断是否复读了words 4遍，符合条件返回True，否则返回False。
    :param words: str
    """
    with open(data_path + 'repeat_temp', 'r', encoding='utf-8') as f:
        words_l = f.readlines()
        print(words_l)
    if words_l[0] != (words + '\n'):
        with open(data_path + 'repeat_temp', 'w', encoding='utf-8') as f:
            f.write(words + '\n')
    elif len(words_l) == 1:
        with open(data_path + 'repeat_temp', 'a', encoding='utf-8') as f:
            f.write(words + '\n')
    elif len(words_l) == 2:
        with open(data_path + 'repeat_temp', 'a', encoding='utf-8') as f:
            f.write(words + '\n')
        return True
    return False


def repeat(words: str) -> None:
    """
    群里复读4次，触发此函数，有1/7概率打断复读，有6/7概率复读。
    """
    is_repeat = words_cmp(words)
    if is_repeat:
        sel = random.randint(0, 6)
        if sel == 0:
            send_group('打断复读', group_id)
        else:
            send_group(words, group_id)
