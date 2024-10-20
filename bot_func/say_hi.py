import random
from bot_func.send import send_group
from bot_func.constant import group_id
from bot_func.erlove import read_name


def hi_group(user_id: int) -> None:
    """
    群聊中有人呼唤“二澪”时，做出回应。
    """
    sel = random.randint(0, 3)
    back = '在'
    if sel == 0:
        back = '在'
    elif sel == 1:
        back = '二澪在哦'
    elif sel == 2:
        back = '怎么了'
    elif sel == 3:
        back = '在的呢~'

    name = read_name(user_id)
    if name != '您':
        back += '，%s' % read_name(user_id)
    send_group(back, group_id)


def morning_group(user_id: int) -> None:
    """
    群聊中有人早安问候时，做出回应。
    """
    sel = random.randint(0, 4)
    back = '早'
    if sel == 0:
        back = '早'
    elif sel == 1:
        back = '哦哈哟'
    elif sel == 2:
        back == '早上好'
    elif sel == 3:
        back = '早上好鸭'
    elif sel == 4:
        back = '哈~哦哈哟'

    name = read_name(user_id)
    if name != '您':
        back += '，%s' % read_name(user_id)
    send_group(back, group_id)


def evening_group(user_id: int) -> None:
    """
    群聊中有人晚安问候时，做出回应。
    """
    sel = random.randint(0, 3)
    back = '晚安'
    if sel == 0:
        back = '晚安'
    elif sel == 1:
        back = '哦呀斯密'
    elif sel == 2:
        back = '晚安好梦'

    name = read_name(user_id)
    if name != '您':
        back += '，%s' % read_name(user_id)

    if sel == 3:
        back = '呼噜呼噜ZZZ'
    send_group(back, group_id)


def what_group() -> None:
    """
    群聊中有人呼唤“二澪”但二澪后面跟空格时（空格后面没有跟指令），做出回应。
    """
    sel = random.randint(0, 2)
    back = '嗯？'
    if sel == 0:
        back = '嗯？'
    elif sel == 1:
        back = '请问有什么事吗？'
    elif sel == 2:
        back = '什么，在想我的事情？'
    send_group(back, group_id)


def poke_group(poke_id: int) -> None:
    """
    群聊中有人戳一戳时，做出回应。
    """
    sel = random.randint(0, 6)
    message_send = '呜呜'
    if sel == 0:
        message_send = '呜呜'
    elif sel == 1:
        message_send = '┭┮﹏┭┮'
    elif sel == 2:
        message_send = '...'
    elif sel == 3:
        message_send = '[CQ:at,qq=%d] ○･｀Д´･ ○' % poke_id
    elif sel == 4:
        message_send = '[CQ:at,qq=%d]\n        👊    👊  👊  欧拉👊   \n👊   👊欧拉    👊 👊   👊   👊   欧拉👊 👊   👊欧拉👊        👊\n   👊     👊  👊欧拉👊   👊   👊\n          欧拉👊   👊 👊   欧拉' % poke_id
    elif sel == 5:
        message_send = '[CQ:at,qq=%d] 💢' % poke_id
    elif sel == 6:
        message_send = '[CQ:at,qq=%d]🤨' % poke_id
    send_group(message_send, group_id)
