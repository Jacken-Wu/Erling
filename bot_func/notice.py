from bot_func.send import send_message, send_private
from bot_func.constant import data_path
import time
import os


def add_notice(add_s: str, user_id: int) -> None:
    """
    添加定时提醒。
    """
    notice_file = data_path + 'notice/notice%d' % user_id

    # 判断文件存不存在
    if os.path.exists(notice_file) == False:
        with open(notice_file, 'w', encoding='utf-8') as f:
            pass

    add_l = add_s.split(maxsplit=1)
    if add_l[0].isdigit() and len(add_l) >= 2:
        time_set_2 = time.time() + int(add_l[0]) * 60  # 时间戳
        time_set = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_set_2))  # 时间
    else:
        add_l = add_s.split(maxsplit=2)
        if len(add_l) >= 3:
            time_set = add_l[0] + ' ' + add_l[1]
            time_set_2 = time.mktime(time.strptime(time_set, "%Y-%m-%d %H:%M:%S"))
        else:
            send_private('语法错误', user_id)
            return 0
    time_now = time.time()
    if time_set_2 > time_now:
        with open(notice_file, 'a', encoding='utf-8') as notice:
            notice.write(time_set + ' ' + add_l[-1] + '\n')
        send_private('列表已添加：' + time_set, user_id)
    else:
        send_private('时间小于当前时间，添加失败', user_id)


def view_notice(user_id: int) -> None:
    """
    查看定时提醒
    """
    notice_file = data_path + 'notice/notice%d' % user_id

    # 判断文件存不存在
    if os.path.exists(notice_file) == False:
        with open(notice_file, 'w', encoding='utf-8') as f:
            pass
    
    with open(notice_file, 'r', encoding='utf-8') as notice:
        notice_list = notice.readlines()
    notice_s = ''
    for i in range(len(notice_list)):
        notice_s += str(i + 1) + '. '
        notice_s += notice_list[i]
    send_private(notice_s, user_id)


def del_notice(num, user_id):
    """
    删除定时提醒
    """
    notice_file = data_path + 'notice/notice%d' % user_id

    # 判断文件存不存在
    if os.path.exists(notice_file) == False:
        with open(notice_file, 'w', encoding='utf-8') as f:
            pass
    
    with open(notice_file, 'r', encoding='utf-8') as notice:
        notice_list = notice.readlines()
    num_2 = int(num) - 1
    if num_2 >= len(notice_list) or num_2 < 0:
        send_private('删除失败，无此条提醒', user_id)
    else:
        with open(notice_file, 'w', encoding='utf-8') as notice:
            for i in range(len(notice_list)):
                if i != num_2:
                    notice.write(notice_list[i])
        send_private('已删除提醒' + num, user_id)


def add_music(add_s: str) -> None:
    """
    添加定时群聊消息，一般用来推歌。
    """
    add_l = add_s.split(maxsplit=1)
    if add_l[0].isdigit() and len(add_l) >= 2:
        time_set_2 = time.time() + int(add_l[0]) * 60  # 时间戳
        time_set = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_set_2))  # 时间
    else:
        add_l = add_s.split(maxsplit=2)
        if len(add_l) >= 3:
            time_set = add_l[0] + ' ' + add_l[1]
            time_set_2 = time.mktime(time.strptime(time_set, "%Y-%m-%d %H:%M:%S"))
        else:
            send_message('语法错误')
            return 0
    time_now = time.time()
    if time_set_2 > time_now:
        with open(data_path + 'music', 'a', encoding='utf-8') as music:
            music.write(time_set + ' ' + add_l[-1] + '\n')
        send_message('music已添加：' + time_set + ' ' + add_l[-1])
    else:
        send_message('时间小于当前时间，添加失败')


def view_music() -> None:
    """
    查看定时群聊消息。
    """
    with open(data_path + 'music', 'r', encoding='utf-8') as music:
        music_list = music.readlines()
    music_s = ''
    for i in range(len(music_list)):
        music_s += str(i + 1) + '. '
        music_s += music_list[i]
    send_message(music_s)


def del_music(num: str) -> None:
    """
    删除定时群聊消息。
    @param num: 定时消息序号
    """
    with open(data_path + 'music', 'r', encoding='utf-8') as music:
        music_list = music.readlines()
    num_2 = int(num) - 1
    if num_2 >= len(music_list) or num_2 < 0:
        send_message('删除失败，无此条music')
    else:
        with open(data_path + 'music', 'w', encoding='utf-8') as music:
            for i in range(len(music_list)):
                if i != num_2:
                    music.write(music_list[i])
        send_message('已删除music' + num)
